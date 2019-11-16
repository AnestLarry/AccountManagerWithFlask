from flask import Flask, request, url_for, render_template, Response,redirect
import os
import urllib.parse
import sys
import base64
import time
import platform
import logging
import amf_globals
import encrypt
import pjsql
app: Flask = Flask(__name__)

log = logging.getLogger(__name__)
fhandler = logging.FileHandler("runserver.log", mode="a+")
fhandler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s <%(funcName)s> %(message)s')
fhandler.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

log.addHandler(fhandler)
log.addHandler(ch)

@app.errorhandler(404)
def index(e):
    return redirect("/page/index")

@app.route("/page/<pagename>/", methods=["GET", "POST"])
def Pages(pagename: str):
    Language: str = request.args.get("language", "")
    if pagename:
        pagenames: dict[str, str] = {
            "index": "index.html",
            "search": "search.html",
            "update": "update_page.html",
            "Restore": "Restore.html",
        }
        if pagename in pagenames.keys():
            if request.method == "POST" and pagename == "Restore":
                upload_db = request.files["db_file"]
                log.critical(
                    "Backup is Uploaded! Uploaded's ip { %(address)s } " % {"address": request.remote_addr})
                if os.path.exists("Database.db"):
                    change_db_file_name()
                upload_db.save("Database.db")
                del upload_db
                if Language == "zh":
                    return render_template("Restore.html", position="Restore", language=Language, Status="上传文件成功!", Date=str(time.strftime(r"%Y-%m-%d--%H-%M-%S")))
                else:
                    return render_template("Restore.html", position="Restore", language=Language, Status="Uploaded file Success!", Date=str(time.strftime(r"%Y-%m-%d--%H-%M-%S")))
            else:
                return render_template(pagenames[pagename], language=Language, position=pagename)
        return render_template("index.html", language=Language)


@app.route("/getAccount/")
def getAccount():
    try:
        return encrypt.getAccount()
    except:
        return "500 Application Error", 500


@app.route("/getPW/")
def getPW():
    return encrypt.getpassword()


@app.route("/Save_Result_to_sql/", methods=["POST"])
def Save_Result_to_sql():
    try:
        if request.form['password'] and request.form["AccountStr"]:
            try:
                if request.form["AddressStr"]:
                    AddressStr: str = base64.b64encode(
                        request.form["AddressStr"].encode()).decode()
                else:
                    AddressStr: str = "Tm9BZGRyZXNz"  # NoAddress
            except:
                AddressStr: str = "Tm9BZGRyZXNz"  # NoAddress
            try:
                Text: str = request.form["Text"].decode()
            except:
                Text: str = "NoValue"  # NoValue
            AccountStr, Password = base64.b64encode(request.form['AccountStr'].encode(
            )).decode(), base64.b64encode(request.form['password'].encode()).decode()

            log.warning("Address { " + request.form["AddressStr"] + " } Account { " +
                        request.form["AccountStr"]+" } Text {" + request.form["Text"]+" }")

            sql: manage_sql = pjsql.manage_sql()
            sql.Save_Result_to_sql(AddressStr, AccountStr, Password, Text)
            del sql
            return "Succ", 200
    except IOError:
        print(IOError)
        return "400 Bad Request", 400


@app.route("/Search_item", methods=["POST"])
def Search_item():
    try:
        if request.form['key'] and request.form["keyword"] and request.form['language']:
            keyword = base64.b64encode(
                request.form["keyword"].encode()).decode()
            key: str = request.form['key']
            if key == "0":
                KeyMode_Str = 'Address'
            elif key == "1":
                KeyMode_Str = 'Account'
            elif key == "2":
                KeyMode_Str = 'Password'
            elif key == "3":
                KeyMode_Str = 'Text'
                keyword = request.form["keyword"]
            else:
                return "400 Bad Request", 400

            log.warning("Search Word { "+keyword +
                        " } Class { " + KeyMode_Str + " }")

            sql: manage_sql = pjsql.manage_sql()
            result: str = sql.Search_Item(
                KeyMode_Str, keyword, request.form['language']) + "<br>Search Time:" + time.strftime("%Y-%m-%d-%H-%M-%S")
            del sql
            return result, 200
    except IOError:
        return "400 Bad Request", 400


@app.route("/Update_Text", methods=["POST"])
def Update_Text():
    try:
        if request.form['DateStr'] and request.form["TextStr"]:
            DateStr, TextStr = base64.b64encode(request.form["DateStr"].encode()).decode(
            ), request.form["TextStr"]

            log.warning(
                "Date { " + request.form['DateStr'] + " } TextStr { "+request.form["TextStr"]+" } ")

            sql: manage_sql = pjsql.manage_sql()
            sql.Update_Text(DateStr, TextStr)
            del sql
            return "Succ", 200
    except:
        return "400 Bad Request", 400


@app.route("/Delete/<Date>")
def Delete(Date: str):
    try:
        if Date:
            Date: str = base64.b64encode(Date.encode()).decode()
            sql: manage_sql = pjsql.manage_sql()
            log.warning(sql.Delete_Item(Date))
            del sql
            return "Succ", 200
    except:
        return "400 Bad Request", 400


@app.route("/Backup/")
def Backup():
    log.critical(
        "Backup is Downloaded! Downloader's ip { "+request.remote_addr+" } ")
    sql: manage_sql = pjsql.manage_sql()
    return Response(sql.Backup_Database(), mimetype="application/octet-stream", headers={"Content-Type": "application/octet-stream", "Content-disposition":
                                                                                         "attachment; filename="+str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db")})


@app.route("/static/<folder>/<filename>")
def staticfile(folder: str, filename: str):
    folder = urllib.parse.unquote(folder)
    filename = urllib.parse.unquote(filename)
    responses: dict[str, dict[str, dict[str, str]]] = {"js": {"mimetype": {"value": "application/x-javascript"}, "headers": {"Content-Type": "application/x-javascript"}},
                                                       "css": {"mimetype": {"value": "text/css"}, "headers": {"Content-Type": "text/css"}},
                                                       "img": {"mimetype": {"value": "application/octet-stream"}, "headers": {"Content-Type": "application/octet-stream"}}
                                                       }
    if folder in ("js", "css", "img") and os.path.exists("static/%(folder)s/%(filename)s" % {"folder": folder, "filename": filename}):
        def getfiledata():
            with open("static/%(folder)s/%(filename)s" % {"folder": folder, "filename": filename}, "rb") as f:
                data = True
                while data:
                    data = f.read(1024*1)
                    yield data
        return Response(getfiledata(), mimetype=responses[folder]["mimetype"]["value"], headers=responses[folder]["headers"])
    else:
        return "404 Page Not Found.", 404


def get_urls(varname: str) -> str:
    if varname in amf_globals.urls:
        return amf_globals.urls[varname]
    return amf_globals.urls["index"]


app.add_template_global(get_urls, "get_urls")


def change_db_file_name() -> bool:
    if platform.system() == "Windows":
        os.system("rename Database.db " +
                  str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db"))
        return True
    elif platform.system() == "Linux":
        os.system("mv Database.db " +
                  str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db"))
        return True
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 2:
        app.run(sys.argv[1], port=sys.argv[2])
    elif len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.debug = True
        app.run()
