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

        self.DESCRIPTIONS=baseinstance.getDescriptionsFromBase(False)
        self.mainDESCRIPTIONS=baseinstance.getmainDescriptionsFromBase()
      
    # def shut(self):
    #     self.isShtut = "true"

    def getCardDescription(self):
        text = "что-то пошло не так. попробуйте ещё раз."

        # Среди всех описаний из базы данных находим наиболее похожее с запрашиваемой Алисой картой
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)
        
        prev_state = self.session_store['state']
        
        # if prev_state == 121:
        #     self.session_store['flags']['from_about'] = True

        buttons = [
            {
                "title": "Да",
                "payload": -2,
                "hide": True
            },
            {
                "title": "Нет",
                "payload": 0, # возврат к контексту
                "hide": True
            }
        ]

        baseinstance = Base()
        if baseinstance.connect():
            if self.session_store['flags']['commandhandler'] == "about_app":
                self.session_store['flags']['from_about'] = True
            self.session_store['flags']['commandhandler'] = "card_info"
            if self.session_store['flags']['return_state'] == None:
                self.session_store['flags']['return_state'] = self.session_store['state']

            text = baseinstance.getCardDescFrombase(card_name)
            self.session_store['flags']['custom_repeat'] = text
            self.session_store['state'] = -1
            self.session_store['buttons'] = buttons
            self.session_store['flags']['last_card_name'] = card_name
        
        return text
        

    def getSkillFromBase(self):
        text = "что-то пошло не так. попробуйте ещё раз."

        # Среди всех описаний из базы данных находим наиболее похожее с запрашиваемой Алисой картой
        card_name = card_recognition(self.DESCRIPTIONS, self.from_Alice)
        
        prev_state = self.session_store['state']

        if self.session_store['flags']['return_state'] != None:
            prev_state = self.session_store['flags']['return_state']

        buttons = [
            {
                "title": "Назад",
                "payload": prev_state,
                "hide": True
            }
        ]

        baseinstance = Base()
        if baseinstance.connect():
            self.session_store['flags']['commandhandler'] = "card_info"
            if self.session_store['flags']['return_state'] == None:
                self.session_store['flags']['return_state'] = self.session_store['state']

            text = baseinstance.getSkillDescFrombase(card_name)
            text = text+ ' чтобы прлдолжить скажите "назад"'
            self.session_store['flags']['custom_repeat'] = text
            self.session_store['state'] = 0
            self.session_store['buttons'] = buttons
            self.session_store['flags']['last_card_name'] = card_name

        return text

    def help_f(self):
        # перейти в 118 состояние и вернуться
        text = "что-то пошло не так. попробуйте ещё раз."

        baseinstance = Base()
        if baseinstance.connect():
            self.session_store['flags']['commandhandler'] = "help"
            self.session_store['flags']['return_state'] = self.session_store['state']
            
            text = baseinstance.getStateOut(118)
            self.session_store['buttons'] = [ { "title": "Назад", "payload": self.session_store['state'], "hide": True } ]
            self.session_store['state'] = 118
        return text
        

    def repeat(self):
        text = "что-то пошло не так. попробуйте ещё раз."
        baseinstance = Base()

        if self.session_store['flags']['custom_repeat'] == None:
            if baseinstance.connect():
                text = baseinstance.getStateOut(self.session_store['state'])
        else:
            text = self.session_store['flags']['custom_repeat']
        
        return text#, "repeat"

    def feedback(self):
        self.session_store['flags']['commandhandler'] = "feedback"
        self.session_store['flags']['return_state'] = self.session_store['state']
        self.session_store['state'] = 123
        return "Расскажите что нужно передать."

    def about(self):
        self.session_store['flags']['commandhandler'] = "about_app"
        self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 119)

    requestSamples = {
            'как работает карта':       getCardDescription,
            'как работает свойство':    getSkillFromBase  ,
            'как работает':               getCardDescription,
            'что делает карта':         getCardDescription,
            'что делает свойство':      getSkillFromBase  ,
            'что делает':               getCardDescription,
            'помощь':                   help_f            ,
            'помоги':                   help_f            ,
            'повтори':                  repeat            ,
            'ещё раз':                  repeat            ,
            'напиши разработчику':      feedback          ,
            'напиши разработчикам':     feedback          ,
            'что ты умеешь':           about             
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
    def scanRequest(self,req:str, session_store, bot, tokens):
        self.bot = bot
        self.session_store = session_store
        text = "Извините, запрос непонятен"
        end = False
        debug = {
            'is main flow'  : False,
            'is subflow start'    : False
        }

        incoming_command = req.lower()
        incoming_command = regex.sub('[,+-]', '', incoming_command)
        debug['incoming_cmd'] = str(incoming_command)

        # проверка ввода для отправки фидбека.
        if self.session_store['flags']['commandhandler'] == 'feedback' \
            and session_store['state'] == 123:
            self.session_store['flags']['feedback'] = incoming_command
            text = "Повторяю." + incoming_command + '. Отправляем?'
            self.session_store['state'] = -3
            self.session_store['buttons'] = [
                { "title": "Да", "payload": -4, "hide": True },
                { "title": "Нет", "payload": -5, "hide": True }
            ]

            return text, end, debug, self.session_store
        
        keystates = [139, 163, 187, 189, 195, 214]
        # громилы / адепты / последователи
        if self.session_store['state'] in keystates:
            mentioned_cards = {
                "Громила": False,
                "Последователь": False,
                "Адепт" : False
            }
            detected = []
            # для всех токенов
            for token in tokens:
                # ищем совпадения среди синонимов
                det = card_recognition(self.mainDESCRIPTIONS[1], token)

                # для адептов громил и последователей
                for orig in mentioned_cards.keys():
                    if det.lower() == orig.lower():
                        mentioned_cards[orig] = True
                        
            debug['mainDESCRIPTIONS'] = self.mainDESCRIPTIONS
            debug['mentioned_cards'] = mentioned_cards
            debug['detected'] = detected
            
            out_descrs = []
            for key in mentioned_cards.keys():
                if mentioned_cards[key]:
                    self.from_Alice = key
                    out_descrs.append(self.getCardDescription())
                    out_descrs.append(" ")
            
            outstr = "Не услышала названия карт. Поптобуйте ещё раз их назвать"
            
            if len(out_descrs) > 0:
                self.session_store['state'] = -10
                outstr = "".join(out_descrs) + "Все ли свойства карт вам понятны?"

            if len(outstr) > 1024:
                outstr = outstr[:1024]

            self.session_store['buttons'] = [
                { "title": "Да", "payload": self.session_store['flags']['state_after_cardHandle'], "hide": True },
                { "title": "Нет", "payload": 144, "hide": True }
            ]

            return outstr, end, debug, self.session_store

        args = {}
        # проверка входа в обработчик вопроса
        for key in self.requestSamples.keys():
            if key == incoming_command[:self.requestLength[key]]:#заменить на findall или на работу по токенам
                arg = str(incoming_command[self.requestLength[key]:])
                args[key] = arg

                if arg != None:
                    self.from_Alice = arg
                    text = self.requestSamples[key](self)
                debug['is subflow start'] = True
                return text, end, debug, self.session_store

        debug['requestSamples'] = self.requestSamples
        if self.session_store['buttons']:
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

            if type(min_distance_item["payload"]) == int:
                next_state = min_distance_item["payload"]
            else:
                next_state = int(str(min_distance_item["payload"])[1:-1])

            text = alicehandler.set_next_state(self.session_store, next_state)

        return text, end, debug, self.session_store


def card_recognition(card_names: list, card_from_Alice: str) -> str:
    card_distance_min = 65000
    #min_distance_idx = len(card_names)

    for i in range(len(card_names)):
        current_distance = Levenshtein.distance(card_names[i], card_from_Alice)
        if card_distance_min > current_distance:
            card_distance_min = current_distance
            min_distance_idx = i
    
    treshhold_condition = card_distance_min < len(card_from_Alice)/2

    ret = card_names[min_distance_idx] if treshhold_condition else ""

    return ret

'''
sample = datarequest()

sample.scanRequest("Алиса, что делает эта карта Дагон")
'''