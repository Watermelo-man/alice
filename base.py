
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
            text = "Простите, не знаю такой карты"

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
                t.next_out_id,\
                outputs.text AS next_out_text\
            FROM t\
            INNER JOIN outputs\
            ON t.next_out_id=outputs.id\
            WHERE t.curOut_id=" + str(current_outId)
        
        cur.execute(query)
        ret = cur.fetchall()

        cur.close()
        self.base.close()
        return ret, ('input_id', 'input_text', 'next_out_id', 'next_out_text'), query #col_descriptions
        
    def getDescriptionsFromBase(self) ->list:
        cur = self.base.cursor()
        query = "SELECT Descriptions.name FROM Descriptions"
        cur.execute(query)
        ret = cur.fetchall()
        
        if ret == None:
            text = "Простите, названия карт и свойств из базы не получены"
            return list()

        res=list()
        for el in ret:
            res.append(el[0])

        cur.close()
        self.base.close()
        return res