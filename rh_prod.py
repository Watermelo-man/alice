


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

    def howcardworks(self, card_from_Alice:str):

        # Среди всех описаний из базы данных находим наиболее похожее с запрашиваемой Алисой картой
        card_name = card_recognition(self.DESCRIPTIONS, card_from_Alice)

        baseinstance = Base()
        baseState = baseinstance.connect()
        if baseState == 0:
            return "не подключились к базе"
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getCardDescFrombase(card_name)
        


    requestSamples = {'как работает карта':howcardworks,'как работает карта':howcardworks,'алиса что делает эта карта':howcardworks,'алиса хватит':shut,'хватит':shut}
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


    def scanRequest(self,req:str):  
        #сканируем команду формы функция - аргумент вот так :
        #сравниваем инпут, отрезая от него предполагаемую функцию по длине строки
        iterator = 0
        requestIsgood = False
    
        for request in self.requestSamples:
            if request == req[:self.requestLength[iterator]]:#заменить на findall или на работу по токенам
                requestIsgood = True

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

        if (requestIsgood == False): 
            text  = "Извините, запрос непонятен"

        if (self.isShtut == "false"):
            answer = [text,"false"]
        elif (self.isShtut == "true"):
            answer = ["До свидания!","true"]    

        return answer


def card_recognition(card_names: list, card_from_Alice: str) -> str:
    card_distance_min = 65000
    #min_distance_idx = len(card_names)

    for i in range(len(card_names)):
        current_distance = Levenshtein.distance(card_names[i], card_from_Alice)
        if card_distance_min > current_distance:
            card_distance_min = current_distance
            min_distance_idx = i
    
    return card_names[min_distance_idx]

    
'''
sample = datarequest()

sample.scanRequest("Алиса, что делает эта карта Дагон")
'''