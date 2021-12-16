import random
import time
import json
import pjsetting
from random import Random

ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation


class EncryptRandom(object):
    def __init__(self) -> None:
        self.__r: Random = random.Random(
            pjsetting.MyCode+time.strftime(r"%Y-%m-%d %H-%M-%S"))

    def get_num(self) -> str:
        return str(digits[self.__r.randrange(0, 10)])

    def get_lowercase(self) -> str:
        return ascii_lowercase[self.__r.randrange(0, 26)]

    def get_uppercase(self) -> str:
        return ascii_uppercase[self.__r.randrange(0, 26)]

    def get_word(self) -> str:
        return str(ascii_letters[self.__r.randrange(0, 52)])

    def get_punctuation(self) -> str:
        return punctuation[self.__r.randrange(0, 32)]

    def get_all(self) -> str:
        return printable[self.__r.randrange(0, 94)]

    def randrange(self, i, j) -> int:
        return self.__r.randrange(i, j)


er = EncryptRandom()


def getAccount() -> str:
    n: int = er.randrange(7, 11)
    AccountStr: str = er.get_word()
    for _ in range(n):
        if er.randrange(0, 2) < 1:
            AccountStr += er.get_word()
        else:
            AccountStr += er.get_num()
    return AccountStr


def __getPassword_1() -> str:
    result: str = ""
    for _ in range(6):
        result += er.get_num()
    return result


def __getPassword_2() -> str:
    n: int = er.randrange(8, 14)
    Password_NumAndWord_Str: str = ""
    for _ in range(n):
        t: int = er.randrange(0, 3)
        if t < 1:
            Password_NumAndWord_Str += er.get_lowercase()
        elif t < 2:
            Password_NumAndWord_Str += er.get_num()
        else:
            Password_NumAndWord_Str += er.get_uppercase()
    return Password_NumAndWord_Str


def __getPassword_3() -> str:
    Password3_Str: str = ""
    for _ in range(10):
        if er.randrange(0, 2) < 1:
            Password3_Str += er.get_word()
        else:
            Password3_Str += er.get_num()
    return Password3_Str+er.get_punctuation()


def __getPassword_max() -> str:
    password_list: list = [er.get_num()] + [er.get_num()] + \
        [er.get_lowercase()] + [er.get_lowercase()] + \
        [er.get_uppercase()] + [er.get_uppercase()] + \
        [er.get_word()] + [er.get_word()] + \
        [er.get_punctuation()] + [er.get_punctuation()] + \
        [er.get_all()] + [er.get_all()]
    for _ in range(8):
        if random.choice([True, False]):
            password_list += [er.get_all()]
    random.shuffle(password_list)
    result_password: str = "".join(password_list)
    return result_password


def getpassword() -> str:
    return json.dumps(
        {"pw1": __getPassword_1(),
         "pw2": __getPassword_2(),
         "pw3": __getPassword_3(),
         "pwmax": __getPassword_max()})
