 
import json

f = open('event.json',encoding='utf-8')
event = json.load(f)

#there starts code for function


from base import *
from meeting import *
from requesthandler import *

    



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