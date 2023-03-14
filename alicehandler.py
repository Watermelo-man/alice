 
import json

f = open('event.json',encoding='utf-8')
event = json.load(f)

#there starts code for function


from base import *
from meeting import *
from requesthandler import *
import telebot    

bot = telebot.TeleBot('6058714565:AAHPhL2Bs_i9lyYaf0bvqcL1e-RkOhH85fU')


Meet = Meeting()

Datarequest = datarequest()

def make_response(event, text, list_arg, next_state = None, end = False):
    if next_state == -1:
        current_state = 96 # Вы уже играли в миры ктулху?
    elif next_state != None:
        current_state = next_state
    else:
        current_state = event["state"]["session"]["state"]

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
    msg += "response: "+ text + "\n\n"
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
            }
        }

# start point
def handler(event,context):
    meetlist = Meet.responseToMeetState(event['session']['new'])

    if meetlist != [None, None]:
        Datarequest.isShtut = "false"
        return make_response(event, meetlist[0], meetlist, -1, meetlist[1])

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['command']) > 0:
        
        request = (event['request']['command'],)
        list_arg = Datarequest.scanRequest(str(request[0]))

        #первое это номер чата
        screen = "screen" in event["meta"]["interfaces"]
        #print(type(event["meta"]["interfaces"]["screen"]))
        #if event["meta"]["interfaces"]["screen"] == {}:
        #    flag = "none"
        msg =   "session id: " + event["session"]["session_id"] + "\n\n"
        msg +=  "user_id: " + event["session"]["user"]["user_id"] + "\n\n"
        msg += "screen: " + str(screen) + "\n\n"
        msg += "request: " + str(event['request']['command']) + "\n\n"
        msg += "response: "+ list_arg[0]
        if (len(list_arg) > 2):
            msg += "debug: "+ query#list_arg[2]
        bot.send_message(-1001609876238 , msg ,message_thread_id = 453)


    #else:
        #session_state['state'] = 1
        return make_response(event, list_arg[0], list_arg, None, list_arg[1])

    return make_response(event, "не обработано", list_arg, None, list_arg[0])

context = None
handler(event,context)