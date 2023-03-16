from base import *

import string
import regex

import Levenshtein

class datarequest():
    data = None
    isShtut = "false"

    def __init__(self) -> None:
        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"

        self.DESCRIPTIONS=baseinstance.getDescriptionsFromBase()

    def setData(self,data):
        self.data = data

    def getData(self):
        return self.data
    
      
    def shut(self):
        self.isShtut = "true"

    def getCardDescription(self, card_from_Alice:str):

        # Среди всех описаний из базы данных находим наиболее похожее с запрашиваемой Алисой картой
        card_name = card_recognition(self.DESCRIPTIONS, card_from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getCardDescFrombase(card_name)
        

    def getSkillFromBase(self,skill_from_Alice:str):
        card_name = card_recognition(self.DESCRIPTIONS, skill_from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getSkillDescFrombase(card_name)


    requestSamples = {'как работает карта':getCardDescription,'как работает свойство':getSkillFromBase,'что делает эта карта':getCardDescription,'что делает':getCardDescription,'алиса хватит':shut,'хватит':shut}
    requestLength = []
    #requestSmaples['Алиса, напиши говно']()
    for key in requestSamples:                  #это не решение, это пиздец. создаем список с длиной каждого ключа
        requestLength.append(len(key))

    '''
    tokenContextField = ['карта', 'навык','работает'] 
    tokenEventField = []
    tokenCardField = ['работает', '']
    tokenSkillField = []

    def tokenscanRequest():
        '''

    # возвращаем текст, флаг выхода, отладочную инфу
    def scanRequest(self,req:str):  
        #сканируем команду формы функция - аргумент вот так :
        #сравниваем инпут, отрезая от него предполагаемую функцию по длине строки

        if (self.isShtut == "true"):
            return "До свидания!", "true", {} # text, endflag, debug
            
        text  = "Извините, запрос непонятен"
        end = "false"
        debug = {}
        
        iterator = 0
        for request in self.requestSamples:
            if request == req[:self.requestLength[iterator]]:#заменить на findall или на работу по токенам
                arg = str(req[self.requestLength[iterator]:].lstrip())


                arg = regex.sub('[,+-]', '', arg)
               
                if arg == "":
                    try:
                        text = self.requestSamples[req[:self.requestLength[iterator]]]() 
                    except TypeError:
                        text = self.requestSamples[req[:self.requestLength[iterator]]](self) 

                if arg != "":
                    text = self.requestSamples[req[:self.requestLength[iterator]]](self,arg) 
                 
                break
            iterator = iterator + 1

        return text, end, debug


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