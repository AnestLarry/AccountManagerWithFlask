import time,random,string
def generate():
    r=random.Random(time.strftime(r"%Y-%m-%d %H-%M-%S"))
    key= lambda x=0:string.printable[r.randrange(0,94)]
    result=""
    for _ in range(18):
        result+=key()
    return result
if __name__ == "__main__":
    print(generate())