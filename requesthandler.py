


from base import *

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

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе", None
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getCardDescFrombase(card_name), "card_info"
        

    def getSkillFromBase(self):
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе", None
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getSkillDescFrombase(card_name), "act_info"

    def help_f(self):
        # перейти в 118 состояние и вернуться
        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе", None

        self.event['state']['session']['flags']['return_state'] = self.event['state']['session']['state']
        self.event['state']['session']['flags']['end_commandhandler'] = True
        self.event['state']['session']['state'] = 118

        return baseinstance.getStateOut(118), "help"
        

    def repeat(self):
        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе", None
        return baseinstance.getStateOut(self.cur_state), "repeat"

    def feedback(self):
        return "ещё не доделали", "feedback"

    def about(self):
        return "ещё не доделали", "about_app"

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
    def scanRequest(self,req:str, current_state, event):
        self.next_state = None
        self.cur_state = current_state
        self.event = event
        #сканируем команду формы функция - аргумент вот так :
        #сравниваем инпут, отрезая от него предполагаемую функцию по длине строки

        # if (self.isShtut == "true"):
        #     return "До свидания!", "true", {} # text, endflag, debug
            
        text = "Извините, запрос непонятен"
        end = "false"
        cmd = None
        debug = {}

        # min_distance_key = self.requestSamples['помощь']
        # card_distance_min = Levenshtein.distance('помощь', req)
        
        # for key in self.requestSamples.keys():
        #     current_distance = Levenshtein.distance(key, req)
        #     if card_distance_min > current_distance:
        #         card_distance_min = current_distance
        #         min_distance_key = key
        
        # if card_distance_min < len(min_distance_key)/2:
        #     text = self.requestSamples[min_distance_key]["func"](self)
        #     cmd = self.requestSamples[min_distance_key]["commandhandler"]
        
        iterator = 0
        for key in self.requestSamples.keys():
            if key == req[:self.requestLength[key]]:#заменить на findall или на работу по токенам
                arg = str(req[self.requestLength[key]:].lstrip())
                
                if arg != None:
                    arg = regex.sub('[,+-]', '', arg)

                if arg != None:
                    self.from_Alice = str(req[self.requestLength[key]:])
                    text, cmd = self.requestSamples[key](self)
                 
                break
            iterator = iterator + 1

        return text, end, debug, cmd, self.next_state


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