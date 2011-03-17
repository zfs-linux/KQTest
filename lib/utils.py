# Copyright (c) 2010 Knowledge Quest Infotech Pvt. Ltd. 
# Produced at Knowledge Quest Infotech Pvt. Ltd. 
# Written by: Knowledge Quest Infotech Pvt. Ltd. 
#             zfs@kqinfotech.com
#
# This software is NOT free to use and you cannot redistribute it
# and/or modify it. You should be possesion of this software only with
# the explicit consent of the original copyright holder.
#
# This is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.

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
    
