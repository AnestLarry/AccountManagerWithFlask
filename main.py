from flask import Flask, request, url_for, render_template, Response, redirect
from typing import Dict
from pjsql import manage_sql
import os
import urllib.parse
import sys
import base64
import time
import logging
import encrypt
import json
import shutil
import pjsetting as PS
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
        if pagename in PS.pageNames.keys():
            if request.method == "POST" and pagename == "Restore":
                upload_db = request.files["db_file"]
                log.critical(
                    "Backup is Uploaded! Uploaded's ip { %(address)s } " % {"address": request.remote_addr})
                if os.path.exists("Database.db"):
                    change_db_file_name()
                upload_db.save("Database.db")
                del upload_db
                return render_template("Restore.html", position="Restore", language=Language, Status="Uploaded file Success!", Date=str(time.strftime(r"%Y-%m-%d--%H-%M-%S")))
            else:
                return render_template(PS.pageNames[pagename], language=Language, position=pagename)
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
            log.warning("Address { %s } Account { %s } Text { %s }" % (
                request.form["AddressStr"], request.form["AccountStr"], request.form["Text"],))
            sql = manage_sql()
            sql.Save_Result_to_sql(AddressStr, AccountStr, Password, Text)
            del sql
            return "Succ", 200
    except IOError:
        print(IOError)
        return "400 Bad Request", 400


@app.route("/Search_item", methods=["POST"])
def Search_item():
    try:
        if request.form.get("key", "") and request.form.get("keyword", ""):
            keyword = base64.b64encode(
                request.form["keyword"].encode()).decode()
            key: str = request.form['key']
            KeyMode_Str: str = {
                "0": "Address", "1": "Account",
                "2": "Password", "3": "Text"}.get(key, "Error")
            if KeyMode_Str == "Error":
                return "400 Bad Request3", 400
            if key == "3":
                keyword = request.form["keyword"]

            log.warning("Search Word { %s } Class { %s }" %
                        (keyword, KeyMode_Str,))
            sql = manage_sql()
            result: list = sql.Search_Item(
                KeyMode_Str, keyword) + [[time.strftime("%Y-%m-%d-%H-%M-%S")]]
            del sql
            return json.dumps(result), 200
        else:
            return json.dumps({"code": "500", "message": "argv error"}), 500
    except IOError:
        return "400 Bad Request 2", 400


@app.route("/Update_Text", methods=["POST"])
def Update_Text():
    try:
        if request.form['DateStr'] and request.form["TextStr"]:
            DateStr, TextStr = base64.b64encode(request.form["DateStr"].encode()).decode(
            ), request.form["TextStr"]

            log.warning("Date { %s } TextStr { %s } " % (
                request.form['DateStr'], request.form["TextStr"],))
            sql = manage_sql()
            sql.Update_Text(DateStr, TextStr)
            del sql
            return time.strftime("%Y-%m-%d--%H-%M-%S"), 200
    except:
        return "400 Bad Request", 400


@app.route("/Delete/<Date>")
def Delete(Date: str):
    try:
        if Date:
            Date = base64.b64encode(Date.encode()).decode()
            sql = manage_sql()
            log.warning(sql.Delete_Item(Date))
            del sql
            return time.strftime("%Y-%m-%d--%H-%M-%S"), 200
    except:
        return "400 Bad Request", 400


@app.route("/Backup/")
def Backup():
    log.critical("Backup is Downloaded! Downloader's ip { %s } " % (
        request.remote_addr,))
    sql = manage_sql()
    return Response(sql.Backup_Database(), mimetype="application/octet-stream", headers={"Content-Type": "application/octet-stream", "Content-disposition": "attachment; filename="+str(time.strftime(r"%Y-%m-%d--%H-%M-%S")+".db")})


@app.route("/static/<folder>/<filename>")
def staticfile(folder: str, filename: str):
    folder = urllib.parse.unquote(folder)
    filename = urllib.parse.unquote(filename)
    responses: Dict[str, Dict[str, Dict[str, str]]] = {
        "js": {"mimetype": {"value": "application/x-javascript"}, "headers": {"Content-Type": "application/x-javascript"}},
        "css": {"mimetype": {"value": "text/css"}, "headers": {"Content-Type": "text/css"}},
        "img": {"mimetype": {"value": "application/octet-stream"}, "headers": {"Content-Type": "application/octet-stream"}}
    }
    if folder in ("js", "css", "img") and os.path.exists("static/%(folder)s/%(filename)s" % {"folder": folder, "filename": filename}):
        def getfiledata():
            with open("static/%(folder)s/%(filename)s" % {"folder": folder, "filename": filename}, "rb") as f:
                data = b"1"
                while data:
                    data = f.read(1024*1)
                    yield data
        resp = Response(getfiledata(
        ), mimetype=responses[folder]["mimetype"]["value"], headers=responses[folder]["headers"])
        resp.headers["cache-control"] = "max-age=3600;"
        return resp
    else:
        return "404 Page Not Found.", 404


def get_urls(varname: str) -> str:
    if varname in PS.routerUrls:
        return PS.routerUrls[varname]
    return PS.routerUrls["index"]


app.add_template_global(get_urls, "get_urls")


def change_db_file_name() -> bool:
    try:
        shutil.move("Database.db", "%s.db" %
                    (time.strftime(r"%Y-%m-%d--%H-%M-%S"),))
        return True
    except:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 2:
        app.run(sys.argv[1], port=sys.argv[2])
    elif len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.debug = True
        app.run()
