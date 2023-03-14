
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