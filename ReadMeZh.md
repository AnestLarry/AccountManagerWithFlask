## Account Manager With Flask
##### 基于 Flask==1.0.2
* 页面: <a href="ReadMe.md">English</a> <a href="ReadMeZh.md">中文</a>

[![LICENSE](https://img.shields.io/badge/License-Apache%20License%202.0-blue.svg)](LICENSE) [![codecov](https://codecov.io/gh/AnestLarry/AccountManagerWithFlask/branch/Ver_4.0.2/graph/badge.svg)](https://codecov.io/gh/AnestLarry/AccountManagerWithFlask)

### 版本 4.1.0

#### 此自述文件可能不适用新的提交，请注意ReadMe的版本。
### 说明
##### Account Manager With Flask 是一个用于生成和保存您的帐户和密码的网页。它可以防止泄露隐私。例如，有人记录你的用户的姓名，帐户或密码。

#### 0. Flask版本与Django版本不完全相同。

#### 1.设置您的设置文件
##### 使用文本编辑器打开pjsetting.py并更改需要更改的变量。
##### 示例：MyCode ="""nR ^ K.Z'_mLLT＃XJSc <"""
##### 解释：
1."MyCode"随机种子
2."sqltype"sql类型，现在只支持"sqlite3"
##### MyCode可以从`Tools/GetMyCode.py`获取

#### 2.获取数据库文件
##### SQLite3：您可以通过`Tools / GetInitDatabaseSqlite3.py`获取示例数据库文件。将数据库文件放在根目录上。其中有一个测试数据，您可以使用`test.com`进行搜索，或者使用'1970-01-01--00-00-00- Thursday`将其删除。

#### 3.运行
##### Windows：
###### 双击`Start.cmd`并打开浏览器到`http：//127.0.0.1：5000`
###### 命令：python main.py ip port
###### 示例：python main.py 127.0.0.1 5000
###### 解释：
ip：需要监听的（默认为127.0.0.1）
port：需要监听的（默认为5000）
##### Linux：
###### 命令：python3 main.py ip port
###### 示例：python3 main.py 127.0.0.1 5000
###### 解释：
ip：需要监听的（默认为127.0.0.1）
port：需要监听的（默认为5000）

#### 4. GUI(win)
##### 运行时: .NET 5
##### IDE: VS2019
双击使用项目生成的`.exe`文件。 只需将其用作webui（需要运行main.py）。