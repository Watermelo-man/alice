


import random
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
            return "не подключились к базе"

        self.DESCRIPTIONS=baseinstance.getDescriptionsFromBase()
    
      
    # def shut(self):
    #     self.isShtut = "true"

    def getCardDescription(self):

        # Среди всех описаний из базы данных находим наиболее похожее с запрашиваемой Алисой картой
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getCardDescFrombase(card_name)
        

    def getSkillFromBase(self):
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getSkillDescFrombase(card_name)

    def help_f(self):
        return "ещё не доделали"

    def repeat(self):
        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"
        return getStateOut(self.cur_state)

    def feedback(self):
        return "ещё не доделали"

    def about(self):
        return "ещё не доделали"

    requestSamples = {
            'как работает карта':       { "func" : getCardDescription,  "commandhandler" : "card_info"    },
            'как работает свойство':    { "func" : getSkillFromBase  ,  "commandhandler" : "act_info"     },
            'что делает эта карта':     { "func" : getCardDescription,  "commandhandler" : "card_info"    },
            'что делает':               { "func" : getCardDescription,  "commandhandler" : "card_info"    },
            'помощь':                   { "func" : help_f            ,  "commandhandler" : "help"         },
            'повтори':                  { "func" : repeat            ,  "commandhandler" : "repeat"       },
            'напиши разработчику':      { "func" : feedback          ,  "commandhandler" : "feedback"     },
            'что ты умеешь?':           { "func" : about             ,  "commandhandler" : "about_app"    }
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
    def scanRequest(self,req:str, current_state):
        self.cur_state = current_state
        #сканируем команду формы функция - аргумент вот так :
        #сравниваем инпут, отрезая от него предполагаемую функцию по длине строки

        # if (self.isShtut == "true"):
        #     return "До свидания!", "true", {} # text, endflag, debug
            
        text = random.choice(["Извините, запрос непонятен",
                              "Вы не могли бы повторить",
                              "Извините, что-то со слухом, повторите пожалуста",
                              "Что-что?"])
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
                    text = self.requestSamples[key]['func'](self)
                 
                break
            iterator = iterator + 1

        return text, end, debug, cmd


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