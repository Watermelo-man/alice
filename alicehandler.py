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
    #print(type(event["meta"]["interfaces"]["screen"]))
    #if event["meta"]["interfaces"]["screen"] == {}:
    #    flag = "none"
    msg =   "session id: " + event["session"]["session_id"] + "\n\n"
    msg +=  "user_id: " + event["session"]["user"]["user_id"] + "\n\n"
    msg += "screen: " + str(screen) + "\n\n"
    msg += "request: " + str(event['request']['command']) + "\n\n"
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
    
    return{
            'version': event['version'],
            'session': event['session'],
            "session_state": session_state,
            'response': {
                'text': text,
                'end_session': end
            },
            'debug' : list_arg
        }

# start point
def handler(event,context):
    # обработка входа в сценарий
    if event['session']['new'] == True:
        Datarequest.isShtut = "false"
        #return make_response(event, 'Вы уже играли в миры ктулху?', [], next_state, False)
        return make_response(event, None, [], start_state, False)

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
        list_arg = Datarequest.scanRequest(str(request[0]))

        #первое это номер чата
        screen = "screen" in event["meta"]["interfaces"]
        #print(type(event["meta"]["interfaces"]["screen"]))
        #if event["meta"]["interfaces"]["screen"] == {}:
        #    flag = "none"
        msg =   "session id: " + event["session"]["session_id"] + "\n\n"
        #msg +=  "user_id: " + event["session"]["user"]["user_id"] + "\n\n"
        msg += "screen: " + str(screen) + "\n\n"
        msg += "request: " + str(event['request']['command']) + "\n\n"
        msg += "response: "+ str(list_arg[0])
        if (len(list_arg) > 2):
            msg += "debug: "+ str(list_arg[2])
        bot.send_message(-1001609876238 , msg ,message_thread_id = 453)


    #else:
        #session_state['state'] = 1
        return make_response(event, list_arg[0], list_arg, 'None', list_arg[1])

    return make_response(event, "не обработано", [], None, list_arg[0])