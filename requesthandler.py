from base import *
import alicehandler
import random
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

        self.accepted = ["да", "ага", "угу", "давай", "рассажи", "хочу",
        "хотим", "перечисли", "да-да", "продолжим", "продолжаем", "играл", "напомни",
        "потребуется", "конечно", "обязательно", "несомненно", "так", "верно", 
        "всё так", "все", "понятны", "ясно", "всё ясно", "понятно", "понял", "появились",
        "готово", "сделано", "погнали", "вперёд", "начинаем", "начнём", "достал",
        "отложил", "посчитал", "сосчитал", "проверил", "получил", "раздал", "положил",
        "раскрыл", "выполнил", "закончил", "взял", "подготовил"]

        self.rejected = ["нет", "неа", "не", "не-не", "не-а", "не надо", "не хочу",
        "не хотим", "не играл", "не потребуется", "не так", "не все", "не понятны",
        "не понял", "не появились", "не появлялись"]

        self.descr_state = {}
        self.descr_state["Громила"] = baseinstance.getStateOut(141, None, False)
        self.descr_state["Последователь"] = baseinstance.getStateOut(140, None, False)
        self.descr_state["Адепт"] = baseinstance.getStateOut(142, None, False)
        
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
        if card_name == None or card_name == "":
            text = "Простите, не расслышала название карты"
        elif baseinstance.connect():
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

    def back(self):
        text = "Сейчас вернуться не получится."
        if self.session_store['flags']['prev_state'] != None:
            text = alicehandler.set_next_state(self.session_store, self.session_store['flags']['prev_state'])
            self.session_store['flags']['prev_state'] = None

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
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']
        self.session_store['state'] = 123
        return "Расскажите что нужно передать."

    def about(self):
        self.session_store['flags']['commandhandler'] = "about_app"
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 119)
    
    def card_example(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 124)

    def howTo_safeLoc(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 236)

    def howTo_shop(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 234)

    def howTo_buy(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 235)

    def howTo_marker(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 240)

    def howTo_gatesLoc(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 238)

    def howTo_simpleLoc(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 237)

    def howTo_mainCards(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 241)

    def howTo_selfCards(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 242)

    def howTo_droppedCards(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 243)

    def howTo_accessedCards(self):
        if self.session_store['flags']['return_state'] == None:
            self.session_store['flags']['return_state'] = self.session_store['state']

        return alicehandler.set_next_state(self.session_store, 244)

    def to_start(self):
        self.session_store['flags'] = {
                'from_about': False,
                'commandhandler' : None,
                'return_state' : None,
                'custom_repeat' : None,
                'last_card_name' : None
            }
        return alicehandler.set_next_state(self.session_store, 106)

    requestSamples = {
            'как работает убежище':         howTo_safeLoc,
            'как работает магазин':         howTo_shop,
            'как работает покупка':         howTo_buy,
            'что такое планшет':            howTo_marker,
            'как работают врата':           howTo_gatesLoc,
            
            'как работает локация':         howTo_simpleLoc,
            'как работают локация':         howTo_simpleLoc,
            'как работает здание':          howTo_simpleLoc,
            'как работают здания':          howTo_simpleLoc,
            'какие бывают локации':         howTo_simpleLoc,
            'какие бывают здания':          howTo_simpleLoc,

            'что такое основная колода':    howTo_mainCards,
            'что такое личная колода':      howTo_selfCards,
            'что такое сброс':              howTo_droppedCards,
            'что такое доступные карты':    howTo_accessedCards,

            'как работает карта':       getCardDescription,
            'как работает свойство':    getSkillFromBase  ,
            'как работает действие':    getSkillFromBase  ,
            'что делает карта':         getCardDescription,
            'что делает свойство':      getSkillFromBase  ,
            'что делает действие':      getSkillFromBase  ,
            'что такое':                getSkillFromBase  ,
            'кто такой':                getSkillFromBase  ,
            'кто такие':                getSkillFromBase  ,
            'что значит':               getSkillFromBase  ,
            'как работает':             getCardDescription,
            'как работают':             getCardDescription,
            'что делает':               getCardDescription,
            'что делают':               getCardDescription,
            'помощь':                   help_f            ,
            'помоги':                   help_f            ,
            'не понимаю':               help_f            ,
            'повтори':                  repeat            ,
            'ещё раз':                  repeat            ,
            'напиши разработчику':      feedback          ,
            'напиши разработчикам':     feedback          ,
            'написать разработчику':    feedback          ,
            'написать разработчикам':   feedback          ,
            'отправить разработчику':   feedback          ,
            'отправить разработчикам':  feedback          ,
            'что ты умеешь':            about             ,
            'расскажи что ты умеешь':   about             ,
            'давай играть':             to_start          ,
            'начать игру':              to_start          ,
            'начни игру':               to_start          ,
            'начни сначала':            to_start          ,
            'давай сыграем':            to_start          ,
            'давай заново':             to_start          ,
            'начать заново':            to_start          ,
            'давай сначала':            to_start          ,
            'какие бывают карты':       card_example      ,
            'какие есть карты':         card_example      ,
            'назад':                    back
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

    def incomingFeedback_handler(self):
        if self.session_store['flags']['commandhandler'] == 'feedback' \
            and session_store['state'] == 123:

            processed = True
            self.session_store['flags']['feedback'] = self.incoming_command
            self.text = "Повторяю. " + self.incoming_command + '. Отправляем?'
            self.session_store['state'] = -3
            self.session_store['buttons'] = [
                { "title": "Да", "payload": -4, "hide": True },
                { "title": "Нет", "payload": -5, "hide": True }
            ]
            self.debug['incomingFeedback_handler'] = True
            raise Exception(True)

    def incomingJoinMainCardDescr_handler(self):
        keystates = [139, 163, 187, 189, 195, 214, 230]
        
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
            
            out_descrs = []
            for key in mentioned_cards.keys():
                if mentioned_cards[key]:
                    out_descrs.append(self.descr_state[key])
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

            self.text = outstr
            self.debug['joinMain'] = True
            raise Exception(True)

    def incomingQuestion_handler(self):
        btn_titles = []
        for btn in self.session_store['buttons']:
            btn_titles.append(btn['title'].lower())

        for key in self.requestSamples.keys():
            if key == self.incoming_command[:self.requestLength[key]]:#заменить на findall или на работу по токенам
                arg = str(self.incoming_command[self.requestLength[key]:])

                self.debug['is subflow start'] = True
                if arg != None and (("назад" in btn_titles) == False):
                    self.from_Alice = arg
                    self.text = self.requestSamples[key](self)
                    debug['incomingQuestion'] = True
                    raise Exception(True)

    def incomingAcceptOrRejrct_handler(self):
        in_accepted = card_recognition(self.accepted, self.incoming_command)
        in_rejected = card_recognition(self.rejected, self.incoming_command)

        if self.session_store['buttons']:
            min_distance_item = self.session_store['buttons'][0]
            min_distance = Levenshtein.distance(min_distance_item['title'].lower(), self.incoming_command)

            for btn in self.session_store['buttons']:
                if (in_accepted != "" and btn['title'].lower() in self.accepted) or \
                    (in_rejected != "" and btn['title'].lower() in self.rejected):
                    min_distance = 0
                    min_distance_item = btn
                    break

                current_distance = Levenshtein.distance(btn['title'].lower(), self.incoming_command)
                if min_distance > current_distance:
                    min_distance = current_distance
                    min_distance_item = btn
            
            treshhold_condition = min_distance < len(self.incoming_command) / 2

            if treshhold_condition:
                if type(min_distance_item["payload"]) == int:
                    next_state = min_distance_item["payload"]
                else:
                    next_state = int(str(min_distance_item["payload"])[1:-1])

                self.text = alicehandler.set_next_state(self.session_store, next_state)
                self.debug['AcceptOrRejrct'] = True
                raise Exception(True)

    # возвращаем текст, флаг выхода, отладочную инфу
    def scanRequest(self,req:str, session_store, bot, tokens):

        # инициализация парсера произвольного ввода
        self.bot = bot
        self.session_store = session_store
        self.text = random.choice(["Извините, запрос непонятен", \
 #                       "Вы не могли бы повторить", \
 #                       "Извините, что-то со слухом, повторите пожалуста", \
                        "Не понимаю"])
        self.end = False
        self.debug = {}
        self.incoming_command = req.lower()
        self.incoming_command = regex.sub('[,+-]', '', self.incoming_command)
        self.debug['incoming_cmd'] = str(self.incoming_command)

        self.debug['wtf'] = 0
        try:
            self.debug['wtf'] = 1
            # проверка ввода для отправки фидбека.
            self.incomingFeedback_handler()
            
            self.debug['wtf'] = 2
            # громилы / адепты / последователи
            self.incomingJoinMainCardDescr_handler()
            
            self.debug['wtf'] = 3
            # обработка входов в обработчики вопросов
            self.incomingQuestion_handler()
            
            self.debug['wtf'] = 4
            # обработка кнопок Да/Нет
            self.incomingAcceptOrRejrct_handler()
            
            self.debug['wtf'] = 5

            # если это не ввод фидбека или ветвления и не вопрос
            # то возможно это просто название карты после "не расслышала название карты"
            self.from_Alice = self.incoming_command
            just_card = self.getCardDescription()
            if just_card != "что-то пошло не так. попробуйте ещё раз."\
                and just_card != "Простите, не расслышала название карты":
                self.text = just_card
        except Exception:
            self.debug['excepted'] = True
        finally:
            self.debug['fin'] = True
            return self.text, self.end, self.debug, self.session_store


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