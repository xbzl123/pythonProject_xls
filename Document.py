
def documentOperation(strpath = "files.txt"):
    f = open(strpath, "r")
    str = f.read()
    print("the content is " + str)
    f.close()
    f = open(strpath, "w")
    f.write(str + ",do not fear!/n")
    f.close()
