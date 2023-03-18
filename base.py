import pymysql

class Base():
    base = None
    
    def __init__(self) -> None:
            pass
    def connect(self,base_source = "alisa_gamerules"):
            try:
                conn = pymysql.connect(
                    user = "user",
                    password="uJ9_ZIOavQ",
                    host="185.171.192.30",
                    port=3306,
                    database=base_source,
                    read_timeout = 1
                )
                self.base = conn
                return 1 #"подключение успешно!"
            
            except pymysql.Error as e:
                return 0 #"не получилось подключиться к БД"
            
    def getCardDescFrombase(self,card:str):
        cur = self.base.cursor()
        query = "SELECT Descriptions.text FROM Descriptions INNER JOIN synonyms ON Descriptions.id=synonyms.description_id WHERE synonyms.synonym= %s"
        cur.execute(query,card)
        ret = cur.fetchone()
        
        if ret != "" and ret != None:
            text = str(ret[0])

        else:
            text = "Простите, не расслышала название карты"

        cur.close()
        self.base.close()
        return text


    def getSkillDescFrombase(self,skill:str):
        cur = self.base.cursor()
        query = "SELECT Descriptions.text FROM Descriptions INNER JOIN synonyms ON Descriptions.id=synonyms.description_id WHERE synonyms.synonym= %s"
        cur.execute(query,skill)
        ret = cur.fetchone()
        
        if ret != "" and ret != None:
            text = str(ret[0])

        else:
            text = "Простите, не расслышала название свойства"

        cur.close()
        self.base.close()
        return text



    def getNextStates(self, current_outId:str, close=True):
        cur = self.base.cursor()
        query = "WITH t AS(\
            SELECT\
                States.outputs_id AS curOut_id,\
                States.inputs_id AS input_id,\
                inputs.text AS input_text,\
                inputs.next_state AS next_out_id\
            FROM States\
            INNER JOIN inputs\
                ON States.inputs_id=inputs.id)\
            SELECT\
                t.input_id,\
                t.input_text,\
                t.next_out_id\
            FROM t\
            INNER JOIN outputs\
            ON t.next_out_id=outputs.id\
            WHERE t.curOut_id=" + str(current_outId)
        
        cur.execute(query)
        ret = cur.fetchall()

        if close:
            cur.close()
            self.base.close()
        return ret, ('input_id', 'input_text', 'next_out_id'), query
        
    def getDescriptionsFromBase(self) ->list:
        cur = self.base.cursor()
        query = "SELECT synonyms.synonym FROM synonyms"
        cur.execute(query)
        ret = cur.fetchall()
        
        if ret == None:
            text = "Названия карт и свойств из базы не получены. Попробуйте позже"
            return list()

        res=list()
        for el in ret:
            res.append(el[0])

        cur.close()
        self.base.close()
        return res

    def getStateOut(self, current_outId:str, session_store = None) -> str:

        if session_store == None:
            cur = self.base.cursor()
            query = "SELECT text FROM outputs WHERE id=" + str(current_outId)
            
            cur.execute(query)
            ret = cur.fetchone()

            cur.close()
            self.base.close()
            return ret[0]
        
        return_text = "чтобы вернуться к игре скажите назад"

        if int(current_outId) == 0:
            return return_text
        
        else:
            if session_store['flags']['commandhandler'] == "card_info":
                if int(current_outId) == -2:
                    if not self.connect():
                        raise Exception("что-то пошло не так, попробуйте ещё раз.")

                    text = self.getCardDetailedDescr(session_store['flags']['last_card_name'])
                    text = text + return_text
                    if len(text) > 1024:
                        text = text[:1024]
                    return text

    def getCardDetailedDescr(self, card):
        cur = self.base.cursor()
        query = "SELECT Descriptions.text FROM Descriptions INNER JOIN( \
        SELECT DISTINCT Features.Feature_type FROM Features INNER JOIN( \
        SELECT card_features.feature_id FROM card_features WHERE \
        card_features.card_name='" + card + "') AS t ON Features.id = t.feature_id \
        ) AS ftr ON ftr.Feature_type=Descriptions.name"
        
        cur.execute(query)
        ret = cur.fetchall()

        cur.close()
        self.base.close()
        if ret == None:
            return None
        else:
            retstring = ""
            for row in ret:
                retstring = retstring + str(row[0])

            if len(retstring) > 1024:
                retstring = retstring[:1024]
                
            return retstring

    def getNextState_byText(self, text:str, currentState:str):
        cur = self.base.cursor()
        query = 'SELECT inputs.next_state from inputs \
        INNER JOIN States ON States.inputs_id = inputs.id \
        WHERE inputs.text="' + str(text) + '" AND States.outputs_id=' + str(currentState)
        
        cur.execute(query)
        ret = cur.fetchone()

        cur.close()
        self.base.close()
        if ret == None:
            return None
        else:
            return ret[0]