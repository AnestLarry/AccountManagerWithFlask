## Account Manager With Flask
##### based on Flask==1.0.2

* Page: <a href="ReadMe.md">English</a> <a href="ReadMeZh.md">中文</a>

[![LICENSE](https://img.shields.io/badge/License-Apache%20License%202.0-blue.svg)](LICENSE) [![codecov](https://codecov.io/gh/AnestLarry/AccountManagerWithFlask/branch/Ver_4.0.2/graph/badge.svg)](https://codecov.io/gh/AnestLarry/AccountManagerWithFlask)

### Version 4.0.2

#### This ReadMe might not apply the new commits , please noticed the Version of ReadMe.
### Description
#### Account Manager With Flask , which is a web to generate and save your account and passswords. It can keep you from Leak privacy .Such as someone log your User's names,Accounts or passwords .

#### 0. Flask versionis not all same with Django version.

#### 1. Set your settings file
##### Open pjsetting.py with text-editor and change vars you need to change.
##### Example : MyCode="""nR^K.Z'_mLLT#XJSc<""" 
##### Explain : 
1. "MyCode" Random Seed
2. "sqltype" sql type ,only suppost "sqlite3" now
##### Or you can use `run me at first.py` to finish your settings file.
##### `run me at first.py` might useless in the new commit

#### 2. Get your Database file
##### SQLite3: you can get the example database file By `Tools/GetInitDatabaseSqlite3.py` . Put your database file on the root. There is a test-data in it and you can search it with `test.com` or delete it by api with `1970-01-01--00-00-00--Thursday`.

#### 3. Run
##### Windows:
###### double click `Start.cmd` and open a browser to `http://127.0.0.1:5000`
###### Command : python main.py ip port
###### Example : python main.py 127.0.0.1 5000
###### Explain:
ip : which was need listened to(default 127.0.0.1)
port : which was need listened to(default 5000)
##### Linux:
###### Command : python3 main.py ip port
###### Example : python3 main.py 127.0.0.1 5000
###### Explain:
ip : which was need listened to(default 127.0.0.1)
port : which was need listened to(default 5000)