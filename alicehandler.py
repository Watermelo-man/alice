
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

# отвечаем пользователю
def make_response(event, text, debug = {}, next_state = None, end = False, isfeedback = False):
    global start_state
    baseinstance = Base()

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

    # отправляем лог
    screen = "screen" in event["meta"]["interfaces"]
    msg =  "session id: " + event["session"]["session_id"] + "\n\n"
    msg += "user_id: " + event["session"]["user"]["user_id"] + "\n\n"
    msg += "screen: " + str(screen) + "\n\n"
    if 'command' in event['request']:
        msg += "request: " + str(event['request']['command']) + "\n\n"
    else:
        msg += "request: button pushed"
    msg += "response: "+ str(text) + "\n\n"
    msg += "current_state=" + str(current_state)
    msg += "\n\ndebug: "+ str(debug)

    bot.send_message(-1001609876238 , msg ,message_thread_id = 453)

    # --- сессионное хранилище
    session_state = {
        'state' : current_state
    }

    context_types = ("start", "cards_preparing", "store_preparing", "first_steps", "game step")
   
    # цепляем предыдущие флаги
    if event["session"]["new"] == False:
        session_state['flags'] = event['state']['session']['flags']
    else:
        session_state['flags'] = \
        {
            'context' : context_types[0],
            'from_about_app' : False, 
            'card_info_explained' : 0 
        }

    # если мы уже не в сценарии сохранить куда возвращаться
    if 'return_state' in session_state['flags']:
        session_state['flags']['return_state'] = session_state['flags']['return_state'];

    if baseinstance.connect():
        next_states, next_states_descr, query = baseinstance.getNextStates(current_state)
    else:
        next_states = []
        next_states_descr = []

    session_state['next_states'] = next_states
    session_state['next_states_col_descr'] = next_states_descr
    
    
    # добавляем кнопки возможных переходов
    buttons = []
    for row in next_states:
        if 'delete' != row[next_states_descr.index('input_text')]:
            buttons.append({ "title": row[next_states_descr.index('input_text')],
            "payload": {row[next_states_descr.index('next_out_id')]}, "hide": True })
    
    # ---


    
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

    COMMANDS = Base().getCommandSynonymsFromBase()

    global start_state 
    # обработка входа в сценарий
    if event['session']['new'] == True:
        Datarequest.isShtut = "false"
        return make_response(event, None, {}, start_state, False)

    # обработка нажатия кнопок
    if event['request']['type'] == "ButtonPressed":
        return make_response(event, None, {}, int(str(event['request']["payload"])[1:-1]), False)

    # обработка произвользого ввода
    if 'request' in event\
        and 'original_utterance' in event['request'] \
        and len(event['request']['command']) > 0:
        
        command = event['request']['command']

        command_synonym = levenshtein_recognition(COMMANDS, command)

        # переходы
        if baseinstance.connect():
            'первое состояние должно быть уже обработано'
            cur_state = event["state"]["session"]["state"]
            next_state = baseinstance.getNextState_byText(command_synonym, cur_state)
            if next_state != None:
                debug = {"next state" :next_state}
                return make_response(event, None, debug, next_state, False)

        # обработка команд
        text, end, debug, isfeedback = Datarequest.scanRequest(str(command))

    return make_response(event, text, debug, None, end , isfeedback)

context = None
handler(event,context)