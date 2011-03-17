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

# ID: grow_pool_001_pos
#
# DESCRIPTION:
# A ZFS file system is limited by the amount of disk space
# available to the pool. Growing the pool by adding a disk
# increases the amount of space.
#
# STRATEGY:
# 1) Fill a ZFS filesystem until ENOSPC by creating a large file
# 2) Grow the pool by adding a disk
# 3) Verify that more data can now be written to the file system
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2005-07-04)
#
# __stc_assertion_end
#
################################################################################

#verify_runnable "global"

import os
import sys
sys.path.append("../../../../lib")
from libtest import *
from logapi import *
from common_variable import *
from grow_pool_cfg import *



#log_assert "A zpool may be increased in capacity by adding a disk"
if not os.geteuid()==0:
        sys.exit("\nOnly root can run this script\n")

if len(sys.argv) not in [2] :
        sys.exit("\nUsage : ./grow_pool_001_pos.ksh <diskname1>\n")
    
log_must([[ZFS,"set","compression=off",TESTPOOL+"/"+TESTFS]])
(data, ret) = cmdExecute([[FILE_WRITE,"-o","create","-f",TESTDIR+"/"+TESTFILE1,"-b",BLOCK_SIZE,"-c",WRITE_COUNT,"-d","0"]]) 

ENOSPC=28

if ret != ENOSPC:
   log_fail("file_write completed w/o ENOSPC, aborting!!!")

if not os.path.exists(TESTDIR+"/"+TESTFILE1):
   log_fail(TESTDIR+"/"+TESTFILE1+" was not created")

DISK = sys.argv[1] 

log_must([[ZPOOL,"add","-f",TESTPOOL,DISK]])

TESTFILE=TESTFILE1

log_must([[FILE_WRITE,"-o","append","-f",TESTDIR+"/"+TESTFILE,"-b",BLOCK_SIZE,"-c",SMALL_WRITE_COUNT,"-d","0"]])
log_must([[ZFS,"inherit","compression",TESTPOOL+"/"+TESTFS]])

log_pass("TESTPOOL successfully grown")

