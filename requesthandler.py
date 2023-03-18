from base import *
import alicehandler

import string
import regex

import Levenshtein

class datarequest():
    # isShtut = "false"

    def __init__(self) -> None:
        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе", None

        self.DESCRIPTIONS=baseinstance.getDescriptionsFromBase()
    
      
    # def shut(self):
    #     self.isShtut = "true"

    def getCardDescription(self):

        # Среди всех описаний из базы данных находим наиболее похожее с запрашиваемой Алисой картой
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)
        
        text = "что-то пошло не так. попробуйте ещё раз."

        baseinstance = Base()
        if baseinstance.connect():
            text = baseinstance.getCardDescFrombase(card_name)
        
        #print(baseinstance.getCardDescFrombase(card))
        return text#, "card_info"
        

    def getSkillFromBase(self):
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе", None
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getSkillDescFrombase(card_name)[0]#, "act_info"

    def help_f(self):
        # перейти в 118 состояние и вернуться
        text = "что-то пошло не так. попробуйте ещё раз."

        baseinstance = Base()
        if baseinstance.connect():
            self.session_store['flags']['commandhandler'] = "help"
            self.session_store['flags']['return_state'] = self.session_store['state']
            self.session_store['state'] = 118
            text = baseinstance.getStateOut(118)

        return text
        

    def repeat(self):
        text = "что-то пошло не так. попробуйте ещё раз."
        
        baseinstance = Base()
        if baseinstance.connect():
            text = baseinstance.getStateOut(self.session_store['state'])
        return text#, "repeat"

    def feedback(self):
        return "ещё не доделали"#, "feedback"

    def about(self):
        return "ещё не доделали"#, "about_app"

    # def commandflow(self, next_state_id):
    #     baseinstance = Base()
    #     baseState = baseinstance.connect()
    #     if baseState == 0:
    #         return "не подключились к базе"

    #     if self.cur_state == 118:
    #         self.event['state']['session']['flags']['end_commandhandler'] = True

    #     text = baseinstance.getStateOut(next_state_id)

    #     self.event['state']['session']['state'] = next_state_id
    #     return text

    requestSamples = {
            'как работает карта':       getCardDescription,
            'как работает свойство':    getSkillFromBase  ,
            'что делает эта карта':     getCardDescription,
            'что делает':               getCardDescription,
            'помощь':                   help_f            ,
            'повтори':                  repeat            ,
            'напиши разработчику':      feedback          ,
            'что ты умеешь?':           about             
            # 'алиса хватит':shut,
            # 'хватит':shut,
        }

    requestLength = {}
    #requestSmaples['Алиса, напиши говно']()
    for key in requestSamples.keys():                  #это не решение, это пиздец. создаем список с длиной каждого ключа
        requestLength[key] = len(key)

    '''
    tokenContextField = ['карта', 'навык','работает'] 
    tokenEventField = []
    tokenCardField = ['работает', '']
    tokenSkillField = []

    def tokenscanRequest():
        '''

    # возвращаем текст, флаг выхода, отладочную инфу
    def scanRequest(self,req:str, session_store):
        self.session_store = session_store
        text = "Извините, запрос непонятен"
        end = False
        debug = {
            'is main flow'  : False,
            'is subflow start'    : False
        }

        incoming_command = req.lower()
        incoming_command = regex.sub('[,+-]', '', incoming_command)

        # проверка входа в обработчик вопроса
        for key in self.requestSamples.keys():
            if key == incoming_command[:self.requestLength[key]]:#заменить на findall или на работу по токенам
                arg = str(incoming_command[self.requestLength[key]:])

                if arg != None:
                    self.from_Alice = arg
                    text = self.requestSamples[key](self)
                debug['is subflow start'] = True
                return text, end, debug, self.session_store


        min_distance_item = self.session_store['buttons'][0]
        min_distance = Levenshtein.distance(min_distance_item['title'].lower(), incoming_command)

        for btn in self.session_store['buttons']:
            current_distance = Levenshtein.distance(btn['title'].lower(), incoming_command)
            if min_distance > current_distance:
                min_distance = current_distance
                min_distance_item = btn
            
        treshhold_condition = min_distance < len(incoming_command) / 2

        if not treshhold_condition:
            return text, end, debug, self.session_store

        next_state = int(str(min_distance_item["payload"])[1:-1])

        text = alicehandler.set_next_state(self.session_store, next_state)
        
        # # проверка переходов по не сценарным кнопкам
        # if 'commandhandler' in event['state']['session']['flags']:
        #     arg = str(req.lstrip())

        #     if arg != None:
        #         arg = regex.sub('[,+-]', '', arg)
        #     debug['is subflow'] = True
        #     debug['subflow cmd'] = arg
        #     debug['last_buttons'] = event['state']['session']['last_buttons']
        #     if arg != None:
        #         for btn in event['state']['session']['last_buttons']:
        #             if btn['title'].lower() == arg:
        #                 text = self.commandflow(int(str(btn['payload'])[1:-1]))
        #                 debug['is sub flow'] = True
        #                 break

        return text, end, debug, self.session_store


def card_recognition(card_names: list, card_from_Alice: str) -> str:
    card_distance_min = 65000
    #min_distance_idx = len(card_names)

    for i in range(len(card_names)):
        current_distance = Levenshtein.distance(card_names[i], card_from_Alice)
        if card_distance_min > current_distance:
            card_distance_min = current_distance
            min_distance_idx = i
    
    treshhold_condition = card_distance_min < len(card_names[min_distance_idx])/2

    ret = card_names[min_distance_idx] if treshhold_condition else ""

    return ret

'''
sample = datarequest()

sample.scanRequest("Алиса, что делает эта карта Дагон")
'''