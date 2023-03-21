
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

    #сортировка кнопок
    sort_buttons = []

    for session_butt_instance in session_store['buttons']:
        if session_butt_instance['title']=='Да':
            sort_buttons.append(session_butt_instance)

    for session_butt_instance in session_store['buttons']:
        if session_butt_instance['title'] == 'Нет':
            sort_buttons.append(session_butt_instance)

    for session_butt_instance in session_store['buttons']:
        if session_butt_instance['title'] != 'Да' and session_butt_instance['title'] != 'Нет':
            sort_buttons.append(session_butt_instance)
    
    session_store['buttons'] = sort_buttons

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
                'from_about': False,
                'commandhandler' : None,
                'return_state' : None,
                'prev_state' : None,
                'custom_repeat' : None,
                'last_card_name' : None,
                'game_context': "hello"
            },
            'buttons' : buttons
        }
        return True, make_response(event, text, [], session_store, end)
    
    return False, {}

def set_next_state(session_store, next_state):
    buttons = []
    prev_state = session_store['state']

    no_back = [0, -1, -2, -3, -4, -5, -10]

    if next_state in no_back:
        session_store['flags']['prev_state'] = None
    else:
        session_store['flags']['prev_state'] = prev_state

    if next_state == session_store['flags']['return_state']:
        session_store['flags']['return_state'] = None

# ------ условные переходы ---------
    if next_state == 139:
        session_store['flags']['state_after_cardHandle'] = 143

    if next_state == 163:
        session_store['flags']['state_after_cardHandle'] = 168

    if next_state == 187:
        session_store['flags']['state_after_cardHandle'] = 184

    if next_state == 189:
        session_store['flags']['state_after_cardHandle'] = 188

    if next_state == 195:
        session_store['flags']['state_after_cardHandle'] = 207

    # if next_state == 188:
    #     session_store['flags']['state_after_cardHandle'] = 204

    if next_state == 214:
        session_store['flags']['state_after_cardHandle'] = 219
        
    if next_state == 230:
        session_store['flags']['state_after_cardHandle'] = 151
# ----------------------------------

    session_store['flags']['custom_repeat'] = None
    if prev_state == 179 or prev_state == 118:
        session_store['flags']['from_about'] = False

    baseinstance = Base()
    if next_state <= 0:
        if session_store['flags']['from_about'] and next_state == 0 and prev_state == -1:
            session_store['flags']['from_about'] = False
            session_store['flags']['commandhandler'] = 'about_app'
            return set_next_state(session_store, 179)

        if next_state == -4 or next_state == -5:
            if next_state == -4:
                bot.send_message(-1001609876238 , session_store['flags']['feedback'] ,message_thread_id = 1896)
            del session_store['flags']['feedback']
            next_state = 0

        try:
            text = baseinstance.getStateOut(next_state, session_store)
        except Exception as e:
            return e
        session_store['flags']['custom_repeat'] = text

        ret_st = session_store['flags']['return_state']
        if session_store['flags']['from_about']:
            ret_st = 179
        buttons.append({ "title": "Назад", "payload": ret_st, "hide": True })
        
        # if session_store['state'] == 0:
        #     session_store['flags']['return_state']
        session_store['state'] = next_state
        session_store['buttons'] = buttons
        return text

    session_store['flags']['from_about'] = False
    session_store['flags']['commandhandler'] = None

    # if session_store['flags']['from_about'] and  prev_state == 0:
    #     session_store['flags']['commandhandler'] = 'about_app'
    #     return set_next_state(session_store, 179)

    # помощь
    if next_state == 118:
        if prev_state == 120:
            buttons.append({ "title": "Назад", "payload": 1, "hide": True })
        else:
            buttons.append({ "title": "Назад", "payload": session_store['flags']['return_state'], "hide": True })

    if next_state == 1:
        if session_store['flags']['game_context'] == 'hello':
            next_state = 178
        else:
            next_state = 177
            buttons.append({ "title": "Да", "payload": session_store['flags']['return_state'], "hide": True })

    if next_state == 144:
        next_next_state = None

        for btn in session_store['buttons']:
            if btn['title'].lower() == "да":
                if type(btn['payload']) == int:
                    next_next_state = btn['payload']
                else:
                    next_next_state = int(str(btn['payload'])[1:-1])
                break

        if next_next_state != None:
            session_store['flags']['return_state'] = next_next_state

    # конец приветствия
    if next_state == 106:
        session_store['flags']['game_context'] = 'preparing'

    # конец подготовки
    if next_state == 137 \
        or next_state == 160 \
        or next_state == 176:
        session_store['flags']['game_context'] = 'game'
    
    # первое состояние "что ты умеещь"
    if next_state == 119 and prev_state == 107:
        session_store['flags']['commandhandler'] = 'about_app'
        session_store['flags']['return_state'] = 99

    if next_state == 126:
        buttons.append({ "title": "Назад", "payload": session_store['flags']['return_state'], "hide": True })

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
    tokens = event['request']['nlu']['tokens']

    text, end, debug, session_store = Datarequest.scanRequest(request, session_store, bot, tokens)
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

