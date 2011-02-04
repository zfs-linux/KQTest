import os
from  lib.KQTest import *

def touch(path):
    printLog("touch "+path)
    fd = open(path,'w')
    fd.close()

def cat(path):
    return cmdQuery(["cat", path])

def stat(filepath):
    printLog("os.stat("+filepath+")\n")
    ret = os.stat(filepath)
    printLog("ret: "+str(ret))
    return ret
    
