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