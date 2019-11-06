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
        self.__c.execute('insert into Data values("'+AddressStr+'","'+AccountStr + '","' + password + '","' +
                         base64.b64encode(time.strftime(r"%Y-%m-%d--%H-%M-%S--%A").encode()).decode()+'","'+Text+'");')
        self.__conn.commit()
        return True

    def Search_Item(self, key: str, keywordStr: str, language: str = "en-us") -> str:
        if key == "Text":
            self.__c.execute(
                'select Address,Account,Password,Date,Text from Data where "'+key+'" in "'+keywordStr+'";')
        else:
            self.__c.execute(
                'select Address,Account,Password,Date,Text from Data where "'+key+'" = "'+keywordStr+'";')
        result_Str: str = '<font size=5>'
        for Item in self.__c.fetchall():
            result_Str += '<table border="1"><tr><td>'+self.__Search_Item_translate_tag(language, "Address")+'</td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[0].encode()).decode()+'"/></td></tr> \
            <tr><td>  '+self.__Search_Item_translate_tag(language, "Account")+' </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[1].encode()).decode()+'"/></td></tr> \
            <tr><td>'+self.__Search_Item_translate_tag(language, "Password")+' </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[2].encode()).decode()+'"/></td></tr>\
            <tr><td>  '+self.__Search_Item_translate_tag(language, "Date")+'  </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[3].encode()).decode()+'"/></td></tr>\
            <tr><td>  '+self.__Search_Item_translate_tag(language, "Text")+'  </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[4].encode()).decode() + '"/></td></tr></table><br>'
        result_Str += '</font>'
        return result_Str

    def __Search_Item_translate_tag(self, language: str, string: str) -> str:
        if language == "zh-cn":
            if string == "Address":
                return "地址"
            elif string == "Account":
                return "帐号"
            elif string == "Password":
                return "密码"
            elif string == "Date":
                return "日期"
            elif string == "Text":
                return "标注"
        else:
            return string

    def Update_Text(self, DateStr: str, TextStr: str) -> bool:
        self.__c.execute('update Data set Text="'+TextStr +
                         '" where Date="'+DateStr + '";')
        self.__conn.commit()
        return True

    def Delete_Item(self, keywordStr: str) -> str:
        self.__c.execute(
            'select Address,Account,Password,Date,Text from Data where "Date" = "'+keywordStr+'";')
        __result: str = ""
        for Item in self.__c.fetchall():
            __result += "Address { "+Item[0]+" } Account { " + \
                Item[1]+"} Password {"+Item[2]+"} Text {"+Item[4]+" }"
        self.__c.execute('delete from Data where Date = "'+keywordStr+'";')
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
