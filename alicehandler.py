 
import json

f = open('event.json',encoding='utf-8')
event = json.load(f)

#there starts code for function


from base import *
from requesthandler import *
import telebot

start_state = 107

bot = telebot.TeleBot('6058714565:AAHPhL2Bs_i9lyYaf0bvqcL1e-RkOhH85fU')

Datarequest = datarequest()

def make_response(event, text, list_arg, next_state = None, end = False):
    if event["state"] and event["state"]["session"] and event["state"]["session"]["state"]:
        current_state = event["state"]["session"]["state"]
    else:
        next_state = start_state
        session_state = {
            'state' : start_state
        }

    baseinstance = Base()

    if next_state != None:
        current_state = next_state
        
        if baseinstance.connect() != 0:
            text = baseinstance.getStateOut(current_state)
        
    session_state = {
        'state' : current_state
    }

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
    if (len(list_arg) > 2):
        msg += "\n\ndebug: "+ str(list_arg[2])
    



    bot.send_message(-1001609876238 , msg ,message_thread_id = 453)

    baseinstance = Base()
    baseState = baseinstance.connect()
    if baseState != 0:
        next_states, next_states_descr, query = baseinstance.getNextStates(current_state)
    else:
        next_states = []
        next_states_descr = []

    session_state['next_states'] = next_states
    session_state['next_states_col_descr'] = next_states_descr
    
    buttons = []
    for row in next_states:
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
            'debug' : list_arg
        }

# start point
def handler(event,context):
    # обработка входа в сценарий
    bot.send_message(-1001609876238 , "request = " + str(event) ,message_thread_id = 453)#debug
    if event['session']['new'] == True:
    # обработка входа в сценарий
    if event['session']['new'] == True:
        Datarequest.isShtut = "false"
        #return make_response(event, 'Вы уже играли в миры ктулху?', [], next_state, False)
        return make_response(event, None, [], start_state, False)

    # обработка нажатия кнопок
    if event['request']['type'] == "ButtonPressed":
        return make_response(event, None, [], int(str(event['request']["payload"])[1:-1]), False)

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['command']) > 0:
        
        request = (event['request']['command'],)

        # обработка переходов
        baseinstance = Base()
        foundNextState = None
        if baseinstance.connect() != 0:
            if (event["state"] and event["state"]["session"] and event["state"]["session"]["state"]):
                cur_state = event["state"]["session"]["state"]
            else:
                cur_state = start_state
            foundNextState = baseinstance.getNextState_byText(request[0], cur_state)
            if foundNextState != None:
                return make_response(event, None, [None,None,str(foundNextState)], foundNextState, False)

        # обработка команд

        # обработка переходов
        baseinstance = Base()
        foundNextState = None
        if baseinstance.connect() != 0:
            if (event["state"] and event["state"]["session"] and event["state"]["session"]["state"]):
                cur_state = event["state"]["session"]["state"]
            else:
                cur_state = start_state
            foundNextState = baseinstance.getNextState_byText(request[0], cur_state)
            if foundNextState != None:
                return make_response(event, None, [None,None,str(foundNextState)], foundNextState, False)
            msg += "debug: "+ str(list_arg[2])
        bot.send_message(-1001609876238 , msg ,message_thread_id = 453)

        # обработка команд
        list_arg = Datarequest.scanRequest(str(request[0]))

        return make_response(event, list_arg[0], list_arg, 'None', list_arg[1])

    return make_response(event, "не обработано", [], None, list_arg[0])
context = None
handler(event,context)