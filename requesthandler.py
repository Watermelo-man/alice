


from base import *

import string
import regex
class datarequest():
    data = None
    isShtut = "false"
    def __init__(self) -> None:
        pass
    def setData(self,data):
        self.data = data
    def getData(self):
        return self.data
    
      
    def shut(self):
        self.isShtut = "true"

    def howcardworks(card:str):

        baseinstance = Base()
        baseState = baseinstance.connect("alisa_gamerules_test")
        if baseState == 0:
            return "не подключились к базе"
        
        #print(baseinstance.getCardDescFrombase(card))
        return baseinstance.getCardDescFrombase(card)
        


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
                    text = self.requestSamples[req[:self.requestLength[iterator]]](arg) 
                 
                break
            iterator = iterator + 1

        if (requestIsgood == False): 
            text  = "Извините, запрос непонятен"

        if (self.isShtut == "false"):
            answer = [text,"false"]
        elif (self.isShtut == "true"):
            answer = ["До свидания!","true"]    

        return answer
                

    
'''
sample = datarequest()

sample.scanRequest("Алиса, что делает эта карта Дагон")
'''