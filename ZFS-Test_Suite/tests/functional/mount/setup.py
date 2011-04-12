#!/usr/bin/python

#copyright (c) 2010 Knowledge Quest Infotech Pvt. Ltd.
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
import sys
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *


FS_CNT=3

TESTFSS=[]
TESTDIRS=[]

def writesetup():
    file = open("mount_cfg.py", 'w')
     
    file.write("TESTFSS="+str(TESTFSS)+"\n")
    file.write("TESTDIRS="+str(TESTDIRS)+"\n")
 
    file.close()

log_onexit(writesetup)

if not os.geteuid()==0:
        sys.exit("\nOnly root can run this script\n")


if len(sys.argv) == 2:
   DISK = sys.argv[1]
   ret = existent_of_disk(DISK)
   if ret != 0 :
     sys.exit("\n Wrong Input..\n")
else :
   sys.exit("\nUsage : Enter the only one argument as disk name\n")


create_pool(TESTPOOL,DISK)
#default_setup(DISK)
log_note("Create file systems with mountpoints, so they are mounted automatically\n")

i = 1

while i <= FS_CNT:
    dir = TESTDIR + "." +str(i)
    fs = TESTPOOL + "/" + TESTFS + "." + str(i)

    ret = log_pos([[RM,"-rf",dir]])
    if ret != SUCCESS :
       log_unresolved("Could not remove "+ dir)

    ret = log_pos([[MKDIR,"-p",dir]])
    if ret != SUCCESS :
       log_unresolved("Could not create "+ dir)
    
    TESTDIRS = TESTDIRS + [dir]   
    
    log_must([[ZFS,"create",fs]])

    log_must([[ZFS,"set","mountpoint="+dir,fs]])

    TESTFSS = TESTFSS + [fs]

    log_note("Make sure file system " + fs + " was mounted")
     
    ret = ismounted(fs)
    if ret != SUCCESS :
       log_fail("File system " + fs +" is not mounted..")

    log_note("Unmount the file system..")

    log_must([[ZFS,"unmount",fs]])

    log_note("Make sure file system " + fs + " is unmounted")
     
    ret = ismounted(fs)
    if ret == SUCCESS :
       log_fail("File system " + fs +" is mounted..")
 
    log_note("File system " + fs +" is unmounted")

    i = i + 1


log_pass("setup done...")
