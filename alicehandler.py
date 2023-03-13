 
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



def handler(event,context):

    

    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
  
    meetlist = Meet.responseToMeetState(event['session']['new'])

    if meetlist != None:
        Datarequest.isShtut = "false"
        return {
            'version': event['version'],
            'session': event['session'],
            #"session_state": session_state,
            'response': {
                # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                'text': meetlist[0],
                # Don't finish the session after this response.
                'end_session': meetlist[1]
            }
        }

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['command']) > 0:
        
        request = (event['request']['command'],)



        list_arg = Datarequest.scanRequest(str(request[0]))
      

        
        #bot.send_message(-1001609876238 , f"тест говна",message_thread_id = 453)
        #первое это номер чата
        flag = "not none"
        #print(type(event["meta"]["interfaces"]["screen"]))
        if event["meta"]["interfaces"]["screen"] == {}:
            flag = "none"
        msg = "session id: " + event["session"]["session_id"] + "\n\n" + "user_id: " + event["session"]["user"]["user_id"] + "\n\n" + "screen: " + flag + "\n\n" + "request: " + str(event['request']['command']) + "\n\n" + "response: "+ list_arg[0]
        bot.send_message(-1001609876238 , msg ,message_thread_id = 453)


    #else:
        #session_state['state'] = 1
    
        return {
            'version': event['version'],
            'session': event['session'],
            #"session_state": session_state,
            'response': {
                # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                'text': list_arg[0],
                # Don't finish the session after this response.
                'end_session': list_arg[1]
            }
        }
    

context = None
handler(event,context)