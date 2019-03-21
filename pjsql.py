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

    def Search_Item(self,key,keywordStr):
        #log.info(request.META['REMOTE_ADDR']+" ["+key+"] ["+keywordStr+"]")
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('select Address,Account,Password,Date,Text from Data where "'+key+'" = "'+keywordStr+'";')
        result_Str='<font size=5>'
        for Item in c.fetchall():
            result_Str+='<table border="1"><tr><td>Address</td><td><input readonly style="width:250px" value="'+base64.b64decode(Item[0].encode()).decode()+'"/></td></tr> \
            <tr><td>  Account  </td><td><input readonly style="width:250px" value="'+base64.b64decode(Item[1].encode()).decode()+'"/></td></tr> \
            <tr><td>  Password  </td><td><input readonly style="width:250px" value="'+base64.b64decode(Item[2].encode()).decode()+'"/></td></tr>\
            <tr><td>  Date  </td><td><input readonly style="width:250px" value="'+base64.b64decode(Item[3].encode()).decode()+'"/></td></tr>\
            <tr><td>  Text  </td><td><input readonly style="width:250px" value="'+base64.b64decode(Item[4].encode()).decode() +'"/></td></tr></table><br>'
        result_Str+='</font>'
        del c,conn
        return result_Str