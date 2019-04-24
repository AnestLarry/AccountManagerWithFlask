import sqlite3,base64,time

class initsql:
    def __init__(self,sqlname):
        if sqlname == "sqlite3":
            self.sqltype = "sqlite3"
        elif sqlname == "mysql":
            self.sqltype = "mysql"
class manage_sql:
    def __init__(self,sqlname="sqlite3"):
        self.__sqltype=sqlname

    def Save_Result_to_sql(self,AddressStr,AccountStr,password,Text):
        #log.info(request.META['REMOTE_ADDR']+" Address { "+AddressStr+" } Account { "+AccountStr+" }")
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('insert into Data values("'+AddressStr+'","'+AccountStr +'","'+ password +'","'+ base64.b64encode( time.strftime(r"%Y-%m-%d--%H-%M-%S--%A").encode() ).decode()+'","'+Text+'");')
        conn.commit()
        del c,conn
        return True

    def Search_Item(self,key,keywordStr,language="en-us"):
        #log.info(request.META['REMOTE_ADDR']+" ["+key+"] ["+keywordStr+"]")
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('select Address,Account,Password,Date,Text from Data where "'+key+'" = "'+keywordStr+'";')
        result_Str='<font size=5>'
        for Item in c.fetchall():
            result_Str+='<table border="1"><tr><td>'+self.__Search_Item_translate_tag(language,"Address")+'</td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[0].encode()).decode()+'"/></td></tr> \
            <tr><td>  '+self.__Search_Item_translate_tag(language,"Account")+' </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[1].encode()).decode()+'"/></td></tr> \
            <tr><td>'+self.__Search_Item_translate_tag(language,"Password")+' </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[2].encode()).decode()+'"/></td></tr>\
            <tr><td>  '+self.__Search_Item_translate_tag(language,"Date")+'  </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[3].encode()).decode()+'"/></td></tr>\
            <tr><td>  '+self.__Search_Item_translate_tag(language,"Text")+'  </td><td><input readonly style="width:250px" onfocus="this.select()" value="'+base64.b64decode(Item[4].encode()).decode() +'"/></td></tr></table><br>'
        result_Str+='</font>'
        del c,conn
        return result_Str
    
    def __Search_Item_translate_tag(self,language,string):
        if language=="zh-cn":
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

    def Update_Text(self,DateStr,TextStr):
        #log.info(request.META['REMOTE_ADDR']+" DateStr{ "+DateStr+" } TextStr { "+TextStr+" }")
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('update Data set Text="'+TextStr+'" where Date="'+DateStr +'";')
        conn.commit()
        del c,conn
        return True
    
    def Delete_Item(self,keywordStr):
        #log.warning(request.META['REMOTE_ADDR']+" "+keywordStr)
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('delete from Data where Date = "'+keywordStr+'";')
        conn.commit()
        del c,conn
        return True

    def Backup_Database(self):
        def getfiledata():
            with open("Database.db","rb") as img:
                data = True
                while data:
                    data = img.read(1024*1)
                    yield data
        return getfiledata()