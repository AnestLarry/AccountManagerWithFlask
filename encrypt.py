import random
import time
import json
import pjsetting
from random import Random

ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation

__r: Random = random.Random(
    pjsetting.MyCode+time.strftime(r"%Y-%m-%d %H-%M-%S"))


def __get_num() -> str: return str(digits[__r.randrange(0, 10)])


def __get_lowercase() -> str: return ascii_lowercase[__r.randrange(0, 26)]


def __get_uppercase() -> str: return ascii_uppercase[__r.randrange(0, 26)]


def __get_word() -> str: return str(ascii_letters[__r.randrange(0, 52)])


def __get_punctuation() -> str: return punctuation[__r.randrange(0, 32)]


def __get_all() -> str: return printable[__r.randrange(0, 94)]


def getAccount() -> str:
    n: int = __r.randrange(7, 11)
    AccountStr: str = __get_word()
    for _ in range(n):
        if __r.randrange(0, 2) < 1:
            AccountStr += __get_word()
        else:
            AccountStr += __get_num()
    return AccountStr


def __getPassword_1() -> str:
    result: str = ""
    for _ in range(6):
        result += __get_num()
    return result


def __getPassword_2() -> str:
    n: int = __r.randrange(8, 14)
    Password_NumAndWord_Str: str = ""
    for _ in range(n):
        t: int = __r.randrange(0, 3)
        if t < 1:
            Password_NumAndWord_Str += __get_lowercase()
        elif t < 2:
            Password_NumAndWord_Str += __get_num()
        else:
            Password_NumAndWord_Str += __get_uppercase()
    return Password_NumAndWord_Str


def __getPassword_3() -> str:
    Password3_Str: str = ""
    for _ in range(10):
        if __r.randrange(0, 2) < 1:
            Password3_Str += __get_word()
        else:
            Password3_Str += __get_num()
    return Password3_Str+__get_punctuation()


def __getPassword_max() -> str:
    password_list: list = [__get_num()] + [__get_num()] + \
        [__get_lowercase()] + [__get_lowercase()] + \
        [__get_uppercase()] + [__get_uppercase()] + \
        [__get_word()] + [__get_word()] + \
        [__get_punctuation()] + [__get_punctuation()] + \
        [__get_all()] + [__get_all()]
    for _ in range(8):
        if random.choice([True, False]):
            password_list += [__get_all()]
    result_password: str = ""
    for _ in range(len(password_list)):
        result_password += password_list.pop(
            random.randint(0, len(password_list)-1))
    return result_password


def getpassword() -> str:
    return json.dumps(
        {"pw1": __getPassword_1(),
         "pw2": __getPassword_2(),
         "pw3": __getPassword_3(),
         "pwmax": __getPassword_max()})
