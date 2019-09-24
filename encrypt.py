import string
import random
import time
import json
import pjsetting

__r = random.Random(pjsetting.MyCode+time.strftime(r"%Y-%m-%d %H-%M-%S"))


def __get_num(x=0): return str(string.digits[__r.randrange(0, 10)])


def __get_lowercase(x=0): return string.ascii_lowercase[__r.randrange(0, 26)]


def __get_uppercase(x=0): return string.ascii_uppercase[__r.randrange(0, 26)]


def __get_word(x=0): return str(string.ascii_letters[__r.randrange(0, 52)])


def __get_punctuation(x=0): return string.punctuation[__r.randrange(0, 32)]


def __get_all(x=0): return string.printable[__r.randrange(0, 94)]


def getAccount():
    n = __r.randrange(7, 11)
    AccountStr = __get_word()
    for _ in range(n):
        if __r.randrange(0, 2) < 1:
            AccountStr += __get_word()
        else:
            AccountStr += __get_num()
    return AccountStr


def __getPassword_1():
    result = ""
    for _ in range(6):
        result += __get_num()
    return result


def __getPassword_2():
    n = __r.randrange(8, 14)
    Password_NumAndWord_Str = ""
    for _ in range(n):
        t = __r.randrange(0, 3)
        if t < 1:
            Password_NumAndWord_Str += __get_lowercase()
        elif t < 2:
            Password_NumAndWord_Str += __get_num()
        else:
            Password_NumAndWord_Str += __get_uppercase()
    return Password_NumAndWord_Str


def __getPassword_3():
    Password3_Str = ""
    for _ in range(10):
        if __r.randrange(0, 2) < 1:
            Password3_Str += __get_word()
        else:
            Password3_Str += __get_num()
    return Password3_Str+__get_punctuation()


def __getPassword_max():
    password_list = [__get_num()] + [__get_num()] + [__get_num()] + \
                    [__get_lowercase()] + [__get_lowercase()] + [__get_lowercase()] + \
                    [__get_uppercase()] + [__get_uppercase()] + [__get_uppercase()] + \
                    [__get_word()] + [__get_word()] + [__get_word()] + \
                    [__get_punctuation()] + [__get_punctuation()] + [__get_punctuation()] + \
                    [__get_all()] + [__get_all()] + [__get_all()]
    result_password = ""
    for _ in range(len(password_list)):
        num_randrange = __r.randrange(len(password_list))
        result_password += password_list.pop(num_randrange)
    return result_password


def getpassword():
    return json.dumps({"pw1": __getPassword_1(),
                       "pw2": __getPassword_2(),
                       "pw3": __getPassword_3(),
                       "pwmax": __getPassword_max()})
