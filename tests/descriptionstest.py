
import pymysql

class Base():
    base = None
    
    def __init__(self) -> None:
            pass
    def connect(self,base_source = "alisa_gamerules_test"):
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
    
    def getDescriptionsFromBase(self):
        cur = self.base.cursor()
        query = "SELECT Descriptions.name FROM Descriptions"
        cur.execute(query)
        ret = cur.fetchall()
        
        if ret != "" and ret != None:
            text = str(ret[0])
        else:
            text = "Простите, не знаю такой карты"
        res=list()
        for el in ret:
            res.append(el[0])
        print(res)
        cur.close()
        self.base.close()
        return text


baseda = Base()

baseda.connect()

baseda.getDescriptionsFromBase()