import sqlite3
import base64
import time


class initsql:
    def __init__(self, sqlname: str):
        if sqlname == "sqlite3":
            self.sqltype = "sqlite3"
        elif sqlname == "mysql":
            self.sqltype = "mysql"


class manage_sql:
    def __init__(self, sqlname: str = "sqlite3", file: str = "Database.db"):
        self.__sqltype: str = sqlname
        self.__conn = sqlite3.connect('Database.db')
        self.__c = self.__conn.cursor()

    def Save_Result_to_sql(self, AddressStr: str, AccountStr: str, password: str, Text: str) -> bool:
        self.__c.execute('insert into Data values(?,?,?,?,?);', (AddressStr, AccountStr,
                                                                 password, base64.b64encode(time.strftime(r"%Y-%m-%d--%H-%M-%S--%A").encode()).decode(), Text))
        self.__conn.commit()
        return True

    def Search_Item(self, key: str, keywordStr: str) -> list:
        if key == "Text":
            self.__c.execute(
                r"select Address,Account,Password,Date,Text from Data where Text LIKE ?;", ("%{}%".format(keywordStr),))
        else:
            self.__c.execute(
                'select Address,Account,Password,Date,Text from Data where {} = ?;'.format(key), (keywordStr,))

        result_List: list = []
        for Item in self.__c.fetchall():
            result_List += [[base64.b64decode(Item[0].encode()).decode(), base64.b64decode(Item[1].encode()).decode(
            ), base64.b64decode(Item[2].encode()).decode(), base64.b64decode(Item[3].encode()).decode(), Item[4]]]

        return result_List

    def Update_Text(self, DateStr: str, TextStr: str) -> bool:
        self.__c.execute(
            'update Data set Text=? where Date=?;', (TextStr, DateStr,))
        self.__conn.commit()
        return True

    def Delete_Item(self, keywordStr: str) -> str:
        self.__c.execute(
            'select Address,Account,Password,Date,Text from Data where Date = ?;', (keywordStr,))
        __result: str = ""
        for Item in self.__c.fetchall():
            __result += "Address [ {} ] Account [ {} ] Password [ {} ] Text [ {} ]".format(
                Item[0], Item[1], Item[2], Item[4])
        self.__c.execute('delete from Data where Date = ?;', (keywordStr,))
        self.__conn.commit()
        return __result

    def Backup_Database(self):
        def getfiledata():
            with open("Database.db", "rb") as img:
                data = True
                while data:
                    data = img.read(1024*1)
                    yield data
        return getfiledata()
