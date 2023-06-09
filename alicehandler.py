
import json

f = open('event.json',encoding='utf-8')
event = json.load(f)

#there starts code for function
from base import *
from requesthandler import *
import telebot

bot = telebot.TeleBot('6058714565:AAHPhL2Bs_i9lyYaf0bvqcL1e-RkOhH85fU')

Datarequest = datarequest()
start_state = 107
#commandhandler = ("help", "repeat", "about_app", "card_info", "act_info", "aobut_cards", "feedback")

# отвечаем пользователю
def make_response(event, text, debug = {}, next_state = None, end = False, command_start = None):
    global start_state
    baseinstance = Base()
    next_states = []
    next_states_descr = []

    if isfeedback:
        bot.send_message(-1001609876238 , "Напиши разработчикам " + text ,message_thread_id = 1896)
        text = "Хорошо, я передам"


    # обработка первого состояния
    if event["session"]["new"]:
        next_state = start_state
        text = None
        if baseinstance.connect():
            text = baseinstance.getStateOut(start_state)
    else:
        current_state = event["state"]["session"]["state"]

    if next_state != None:
        current_state = next_state
        
        if baseinstance.connect():
            text = baseinstance.getStateOut(current_state)
        
    # здесь current_state уже точно существует

    # отправляем лог
    screen = "screen" in event["meta"]["interfaces"]
    #msg =  "session id: " + event["session"]["session_id"] + "\n\n"
    #msg += "user_id: " + event["session"]["user"]["user_id"] + "\n\n"
    msg = "screen: " + str(screen) + "\n\n"
    if 'command' in event['request']:
        msg += "request: " + str(event['request']['command']) + "\n\n"
    else:
        msg += "request: button pushed"
    msg += "response: "+ str(text) + "\n\n"
    msg += "current_state=" + str(current_state)
    #msg += "\n\ndebug: "+ str(debug)

    bot.send_message(-1001609876238 , msg ,message_thread_id = 453)

# --- сессионное хранилище
    session_state = {
        'state' : current_state
    }

    #context_types = ("start", "cards_preparing", "store_preparing", "first_steps", "game step")
   
    # цепляем предыдущие флаги
    if event["session"]["new"] == False:
        session_state['flags'] = event['state']['session']['flags']
    else:
        # в первом состоянии - инициализируем
        session_state['flags'] = \
        {
            'context' : "start",
            'from_about_app' : False, 
            'card_info_explained' : 0 
        }

    # если мы уже не в сценарии
    if 'return_state' in session_state['flags']:
        # и если это не последнее состояние обработчика
        if not 'end_commandhandler' in session_state['flags'] \
            or session_state['flags']['end_commandhandler'] == False:
            # если выходим в "что ты умеешь?"
            if (session_state['flags']['from_about_app']):
                current_state = 120
                if baseinstance.connect():
                    text = baseinstance.getStateOut(current_state)
                session_state['flags']['from_about_app'] = False
                session_state['flags']['commandhandler'] = "about_app"
            # если выходим в сценарий - убираем commandhandler
            else:
                del session_state['flags']['commandhandler']

    # если заходим в обработчик "вопроса" - ставим commandhandler
    if command_start != None:
        session_state['flags']['commandhandler'] = command_start
        # если заходим не из сценария - сохраняем куда возвращаться
        if not 'return_state' in session_state['flags']:
            session_state['flags']['return_state'] = current_state
# ---
    
    # добавляем кнопки возможных переходов
    buttons = []
    if baseinstance.connect():
        next_states, next_states_descr, query = baseinstance.getNextStates(current_state)  
        for row in next_states:
            if 'delete' != row[next_states_descr.index('input_text')]:
                buttons.append({ "title": row[next_states_descr.index('input_text')],
                "payload": {row[next_states_descr.index('next_out_id')]}, "hide": True })


    
    return{
            'version': event['version'],
            'session': event['session'],
            "session_state": session_state,
            'response': {
                'text': text,
                "buttons": buttons,
                'end_session': end
            },
            'debug' : debug
        }

# start point
def handler(event,context):
    text = "не обработано"
    debug = {}
    baseinstance = Base()

    # отправляем лог реквеста (возможно это вносит вклад в падения по таймауту)
    # можно подумать про формирование отдельного потока для отправки логов
    #bot.send_message(-1001609876238 , "request = " + str(event) ,message_thread_id = 453)#debug

    global start_state 
    # обработка входа в сценарий
    if event['session']['new'] == True:
        #Datarequest.isShtut = "false"
        return make_response(event, None, {}, start_state, False)

    # обработка нажатия кнопок
    if event['request']['type'] == "ButtonPressed":
        return make_response(event, None, {}, int(str(event['request']["payload"])[1:-1]), False)

    # обработка произвользого ввода
    if 'request' in event\
        and 'original_utterance' in event['request'] \
        and len(event['request']['command']) > 0:
        
        command = event['request']['command']

        # переходы
        if baseinstance.connect():
            'первое состояние должно быть уже обработано'
            COMMANDS = baseinstance.getCommandSynonymsFromBase()
            command_synonym = levenshtein_recognition(COMMANDS, command)

            cur_state = event["state"]["session"]["state"]
            next_state = baseinstance.getNextState_byText(command_synonym, cur_state)
            if next_state != None:
                debug = {"next state" :next_state}
                return make_response(event, None, debug, next_state, False)

        # обработка команд
        text, end, debug, cmd = Datarequest.scanRequest(str(command), event["state"]["session"]["state"])

    return make_response(event, text, debug, None, end, cmd)

context = None
handler(event,context)