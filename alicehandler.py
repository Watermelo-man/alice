from base import *
from requesthandler import *
import telebot

bot = telebot.TeleBot('6058714565:AAHPhL2Bs_i9lyYaf0bvqcL1e-RkOhH85fU')

Datarequest = datarequest()
start_state = 107
#commandhandler = ("help", "repeat", "about_app", "card_info", "act_info", "aobut_cards", "feedback", "end")

# отвечаем пользователю
def make_response(event, text, debug = {}, next_state = None, end = False, command_start = None):
    global start_state
    baseinstance = Base()
    next_states = []
    next_states_descr = []

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
        # что закомментировано выставляется в requesthandler
        session_state['flags'] = \
        {
            'context' : "start",
            'from_about_app' : False,
            'card_info_explained' : False
            # return_state
            # end_commandhandler
        }

    is_cmd_end = not( not 'end_commandhandler' in session_state['flags'] \
            or session_state['flags']['end_commandhandler'] == False)

    commandhandler_del = False
    # если мы уже не в сценарии
    if 'return_state' in session_state['flags']:
        # и если это последнее состояние обработчика
        if is_cmd_end:
            # если выходим в "что ты умеешь?"
            if (session_state['flags']['from_about_app']):
                current_state = 120
                if baseinstance.connect():
                    text = baseinstance.getStateOut(current_state)
                session_state['flags']['from_about_app'] = False
                session_state['flags']['commandhandler'] = "about_app"
            # если выходим в сценарий - убираем commandhandler
            elif 'commandhandler' in session_state['flags']:
                del session_state['flags']['commandhandler']
                commandhandler_del = True


    # если заходим в обработчик "вопроса" - ставим commandhandler
    if command_start != None or is_cmd_end:
        if not commandhandler_del:
            session_state['flags']['commandhandler'] = command_start
        # если заходим не из сценария - сохраняем куда возвращаться
        if not 'return_state' in session_state['flags']:
            session_state['flags']['return_state'] = current_state
# ---
    
    # добавляем кнопки возможных переходов
    buttons = []

    bot.send_message(-1001609876238 , "is_cmd_end = "+str(is_cmd_end) ,message_thread_id = 453)
    if is_cmd_end:
        if event["session"]["new"] == False:
            buttons.append({ "title": "Вернуться", "payload": {session_state['flags']['return_state']}, "hide": True })
            del session_state['flags']['return_state']
            del session_state['flags']['end_commandhandler']
    else:
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

        cmd_synonims = {
            "Да" : ('да', 'хорошо', 'ага', 'ладно'),
            "Нет" : ('нет', 'неа', 'не-а', 'не хочу')
        }

        command = event['request']['command']

        card_distance_min = 65000
        for key in cmd_synonims.keys:
            # сравниваем Левенштейном command и cmd_synonims
            # command = самое пиздатое совпадение
            for el in cmd_synonims[key]:
                current_distance = Levenshtein.distance(el, command)
                if card_distance_min > current_distance:
                    card_distance_min = current_distance
                    min_distance_key = key
        command = min_distance_key

        # выходы из команд
        if 'end_commandhandler' in event['state']['session']['flags'] \
            and event['state']['session']['flags']['end_commandhandler'] == True:
            #next_state = event['state']['session']['flags']['return_state']
            return make_response(event, None, {}, next_state)

        # переходы
        if baseinstance.connect():
            'первое состояние должно быть уже обработано'
            cur_state = event["state"]["session"]["state"]
            next_state = baseinstance.getNextState_byText(command, cur_state)
            if next_state != None:
                debug = {"next state" :next_state}
                return make_response(event, None, debug, next_state)

        # обработка команд
        text, end, debug, cmd, next_state = Datarequest.scanRequest(str(command), event["state"]["session"]["state"], event)

    return make_response(event, text, debug, next_state, end, cmd)