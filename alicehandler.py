from base import *
from requesthandler import *
import telebot

bot = telebot.TeleBot('6058714565:AAHPhL2Bs_i9lyYaf0bvqcL1e-RkOhH85fU')
Datarequest = datarequest()


def send_log(event, text):
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
    msg += "current_state=" + str(event['state']['session']['state'])
    #msg += "\n\ndebug: "+ str(debug)

    bot.send_message(-1001609876238 , msg ,message_thread_id = 453)

def make_response(event, text, debug, session_store, end = False):
    send_log(event, text)
    return{
            'version': event['version'],
            'session': event['session'],
            'session_state': session_store,
            'response': {
                'text': text,
                'buttons': session_store['buttons'],
                'end_session': end
            },
            'debug' : debug
        }

# обработка входа в сценарий
def session_start_handler(event):
    start_state = 107

    if event['session']['new']:
        buttons = []
        end = False
        event['state']['session']['state'] = 107

        # добавление кнопок из базы
        baseinstance = Base()
        if baseinstance.connect():
            next_states, next_states_descr, query = baseinstance.getNextStates(start_state, False)
            for row in next_states:
                if 'delete' != row[next_states_descr.index('input_text')]:
                    buttons.append({ "title": row[next_states_descr.index('input_text')],
                    "payload": {row[next_states_descr.index('next_out_id')]}, "hide": True })
            text = baseinstance.getStateOut(str(start_state))
        else:
            text = "что-то пошло не так. попробуйте зайти позже"
            end = True
        
        session_store = {
            'state' : start_state,
            'flags' : {
                'commandhandler' : None,
                'return_state' : None,
                'custom_repeat' : None,
                'last_card_name' : None
            },
            'buttons' : buttons
        }
        return True, make_response(event, text, [], session_store, end)
    
    return False, {}

def set_next_state(session_store, next_state):
    buttons = []

    session_store['flags']['custom_repeat'] = None

    baseinstance = Base()
    if next_state <= 0:
        try:
            text = baseinstance.getStateOut(next_state, session_store)
        except Exception as e:
            return e
        session_store['flags']['custom_repeat'] = text
        buttons.append({ "title": "Назад", "payload": session_store['flags']['return_state'], "hide": True })
        
        # if session_store['state'] == 0:
        #     session_store['flags']['return_state']

        session_store['state'] = next_state
        session_store['buttons'] = buttons
        return text

    if next_state == 118:
        buttons.append({ "title": "Назад", "payload": session_store['flags']['return_state'], "hide": True })
        session_store['buttons'] = buttons

    # if session_store['flags']['commandhandler'] != None:
    #     # программное добавление кнопок
    #     buttons.append({ "title": "Вернуться", "payload": session_store['flags']['return_state'], "hide": True })
    # else:
        # добавление кнопок из базы
    baseinstance = Base()
    if baseinstance.connect():
        next_states, next_states_descr, query = baseinstance.getNextStates(next_state, False)
        for row in next_states:
            if 'delete' != row[next_states_descr.index('input_text')]:
                buttons.append({ "title": row[next_states_descr.index('input_text')],
                "payload": {row[next_states_descr.index('next_out_id')]}, "hide": True })
        text = baseinstance.getStateOut(str(next_state))
    else:
        return "что-то пошло не так. попробуйте ещё раз."
    
    session_store['state'] = next_state
    session_store['buttons'] = buttons
    return text


def button_clicked_handler(event, session_store):
    if event['request']['type'] != "ButtonPressed":
        return False, {}

    if type(event['request']['payload']) ==int:
        next_state = event['request']['payload']
    else:
        next_state = int(str(event['request']['payload'])[1:-1])

    text = set_next_state(session_store, next_state)
    
    return True, make_response(event, text, [], session_store, False)



# start point
def handler(event,context):
    # обработка входа в сценарий
    ok, response = session_start_handler(event)
    if ok: return response

    session_store = event['state']['session']
    # обработка нажатия кнопок
    ok, response = button_clicked_handler(event, session_store)
    if ok: return response

    #обработка произвольного ввода        
    request = event['request']['command']

    text, end, debug, session_store = Datarequest.scanRequest(request, session_store, bot)
    return make_response(event, text, debug, session_store, end)

    # # обработка переходов
    # baseinstance = Base()
    # foundNextState = None
    # if baseinstance.connect() != 0:
    #     if (event["state"] and event["state"]["session"] and event["state"]["session"]["state"]):
    #         cur_state = event["state"]["session"]["state"]
    #     else:
    #         cur_state = start_state
    #     foundNextState = baseinstance.getNextState_byText(request[0], cur_state)
    #     if foundNextState != None:
    #         return make_response(event, None, [None,None,str(foundNextState)], foundNextState, False)

    # # обработка команд
    # list_arg = Datarequest.scanRequest(request)

    # return make_response(event, list_arg[0], list_arg, None, list_arg[1])