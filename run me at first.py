with open("pjsetting.py","w",encoding="utf-8") as pjs:
    MyCode=input("MyCode (if none,well get it from tool auto) = ")
    if not MyCode:
        import Tools.GetMyCode
        MyCode=Tools.GetMyCode.generate()
    MyCode="MyCode = \"\"\""+ MyCode +"\"\"\""
    sqltype=input("sql type (Auto sqlite3,not suppost all database) = ")
    if not sqltype:
        sqltype="sqlite3"
    sqltype="sqltype = \"\"\""+ sqltype +"\"\"\""