from flask import Flask,request,url_for,render_template ,Response
import os,urllib.parse ,sys ,base64 ,time , platform
import amf_globals , encrypt ,pjsql
app = Flask(__name__)

@app.route("/")
def index():
    if request.args.get("language","") == "zh":
        return render_template("index.html",language="zh")
    else:
        return render_template("index.html")

@app.route("/search/")
def search():
    if request.args.get("language","") == "zh":
        return render_template("search.html",language="zh",position="search")
    else:
        return render_template("search.html",position="search")

@app.route("/update/")
def update():
    if request.args.get("language","") == "zh":
        return render_template("Update.html",language="zh",position="update")
    else:
        return render_template("Update.html",position="update")

@app.route("/getAccount/")
def getAccount():
    try:
        return encrypt.getAccount()
    except:
        return "500 Application Error",500

@app.route("/getPD/<pdmode>")
def getPD(pdmode):
    try:
        if pdmode == "1" :
            return encrypt.getPassword_1()
        elif pdmode == "2" :
            return encrypt.getPassword_2()
        elif pdmode == "3" :
            return encrypt.getPassword_3()
        elif pdmode == "4" :
            return encrypt.getPassword_max()
    except:
        return "500 Application Error",500

@app.route("/Save_Result_to_sql",methods=["POST"])
def Save_Result_to_sql():
    try:
        if request.form['password'] and request.form["AccountStr"]:
            try:
                AddressStr =base64.b64encode(request.form["AddressStr"].encode()).decode()
            except:
                AddressStr = "Tm9BZGRyZXNz" #NoAddress
            try:
                Text=base64.b64encode(request.form["Text"].decode()).decode()
            except:
                Text="Tm9WYWx1ZQ==" # NoValue
            AccountStr,Password =base64.b64encode(request.form['password'].encode()).decode() , base64.b64encode(request.form['password'].encode()).decode()
            sql=pjsql.manage_sql()
            sql.Save_Result_to_sql(AddressStr,AccountStr,Password,Text)
            del sql
            return "Succ",200
    except:
        return "400 Bad Request",400

@app.route("/Search_item",methods=["POST"])
def Search_item():
    try:
        if request.form['key'] and request.form["keyword"]:
            keyword = base64.b64encode(request.form["keyword"].encode()).decode()
            key=request.form['key']
            if key == "0":
                KeyMode_Str='Address'
            elif key == "1":
                KeyMode_Str='Account'
            elif key == "2":
                KeyMode_Str='Password'
            else:
                return "400 Bad Request",400
            sql=pjsql.manage_sql()
            result=sql.Search_Item(KeyMode_Str,keyword)
            del sql
            return result,200
    except:
        return "400 Bad Request",400

@app.route("/Update_Text",methods=["POST"])
def Update_Text():
    try:
        if request.form['DateStr'] and request.form["TextStr"]:
            DateStr,TextStr = base64.b64encode(request.form["DateStr"].encode()).decode() , base64.b64encode(request.form["TextStr"].encode()).decode()
            sql=pjsql.manage_sql()
            sql.Update_Text(DateStr,TextStr)
            del sql
            return "Succ",200
    except:
        return "400 Bad Request",400

@app.route("/Delete/<Date>")
def Delete(Date):
    try:
        if Date:
            Date=base64.b64encode(Date.encode()).decode()
            sql=pjsql.manage_sql()
            sql.Delete_Item(Date)
            del sql
            return "Succ",200
    except:
        return "400 Bad Request",400

@app.route("/Backup/")
def Backup():
    sql=pjsql.manage_sql()
    return Response(sql.Backup_Database(),mimetype="application/octet-stream",headers={"Content-Type":"application/octet-stream","Content-disposition":
        "attachment; filename="+str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db")})

@app.route("/Restore/",methods=["GET","POST"])
def Restore():
    if request.method == "POST":
        upload_db = request.files["db_file"]
        if os.path.exists("Database.db"):
            change_db_file_name()
        upload_db.save("Database.db")
        del upload_db
        return render_template("Restore.html",position="Restore",language=request.args.get("language",""),Status="Uploaded file Success!",Date=str(time.strftime(r"%Y-%m-%d--%H-%M-%S")))
    if request.args.get("language","") == "zh":
        return render_template("Restore.html",position="Restore",language="zh")
    else:
        return render_template("Restore.html",position="Restore")

@app.route("/static/js/<filename>")
def jsfile(filename):
    filename=urllib.parse.unquote(filename)
    if os.path.exists("static/js/"+filename):
        def getfiledata():
            with open("static/js/"+filename,"rb") as js:
                data = True
                while data:
                    data = js.read(1024*1)
                    yield data
        return Response(getfiledata(),mimetype="application/x-javascript",headers={"Content-Type":"application/x-javascript"})

@app.route("/static/css/<filename>")
def cssfile(filename):
    filename=urllib.parse.unquote(filename)
    if os.path.exists("static/css/"+filename):
        def getfiledata():
            with open("static/css/"+filename,"rb") as css:
                data = True
                while data:
                    data = css.read(1024*1)
                    yield data
        return Response(getfiledata(),mimetype="text/css",headers={"Content-Type":"text/css"})

@app.route("/static/img/<filename>")
def imgfile(filename):
    filename=urllib.parse.unquote(filename)
    if os.path.exists("static/img/"+filename):
        def getfiledata():
            with open("static/img/"+filename,"rb") as img:
                data = True
                while data:
                    data = img.read(1024*1)
                    yield data
        return Response(getfiledata(),mimetype="application/octet-stream",headers={"Content-Type":"application/octet-stream"})



def get_urls(varname):
    if varname in amf_globals.urls:
        return amf_globals.urls[varname]
    return amf_globals.urls["index"]
app.add_template_global(get_urls,"get_urls")

def change_db_file_name():
    if platform.system() == "Windows":
        os.system("rename Database.db "+str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db"))
    elif platform.system() == "Linux":
        os.system("mv Database.db "+str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db"))
    else:
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        app.run(sys.argv[1],port=sys.argv[2])
    elif len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.debug = True
        app.run()
