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
                    database=base_source
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



    def getNextStates(self, current_outId:str):
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
    
    def getCommandSynonymsFromBase(self) ->list:
        cur = self.base.cursor()
        query = "SELECT command_synonyms.synonym FROM command_synonyms"
        cur.execute(query)
        ret = cur.fetchall()
        
        if ret == None:
            text = "Названия команд из базы не получены. Попробуйте позже"
            return list()

        res=list()
        for el in ret:
            res.append(el[0])

        cur.close()
        self.base.close()
        return res

    def getStateOut(self, current_outId:str) -> str:
        cur = self.base.cursor()
        query = "SELECT text FROM outputs WHERE id=" + str(current_outId)
        
        cur.execute(query)
        ret = cur.fetchone()

        cur.close()
        self.base.close()
        return ret[0]

    def getNextState_byText(self, text:str, currentState:str):
        

        cur = self.base.cursor()
        query = 'SELECT t.input_next_state\
                FROM (SELECT inputs.next_state AS input_next_state, inputs.id AS input_id\
                    FROM inputs\
                    INNER JOIN command_synonyms ON command_synonyms.command=inputs.text\
                    WHERE command_synonyms.synonym='+str(text)+\
                    ')\
                AS t INNER JOIN States ON States.inputs_id=t.input_id\
                WHERE States.outputs_id='+str(currentState)
        
        cur.execute(query)
        ret = cur.fetchone()

        cur.close()
        self.base.close()
        if ret == None:
            return None
        else:
            return ret[0]