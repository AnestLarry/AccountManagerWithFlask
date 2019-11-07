# It is important that change the Text to string not a base64-like string.
# base64-like string is not support to search by like.
# and this function is not secure.
# At last , this pyfile is change Text base64-like to string
# 3.4 to 4.1 or 4.0 to 4.1

import os.path
import sqlite3
import base64
if not os.path.exists("Database.db"):
    print("Database file is not existed!")
else:
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    c.execute('select Date,Text from Data;')
    result = []
    for Item in c.fetchall():
        result += ["update Data set Text = \""+base64.b64decode(
            Item[1].encode()).decode()+"\" where Date = \""+Item[0]+"\";"]
    for i in result:
        c.execute(i)
    conn.commit()
    c.execute("update Note set Note2 = '4.1' where Note1 = 'Version';")
    conn.commit()
    conn.close()
    del conn, c
    print("Succ")
