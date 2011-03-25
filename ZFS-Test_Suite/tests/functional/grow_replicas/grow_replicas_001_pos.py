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


###############################################################################
#
# __stc_assertion_start
#
# ID: grow_replicas_001_pos
#
# DESCRIPTION:
# A ZFS file system is limited by the amount of disk space
# available to the pool. Growing the pool by adding a disk
# increases the amount of space.
#
# STRATEGY:
# 1) Fill a ZFS filesystem mirror/raidz until ENOSPC by creating lots
# of files
# 2) Grow the mirror/raidz by adding a disk
# 3) Verify that more data can now be written to the file system
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2005-10-04)
#
# __stc_assertion_end
#
################################################################################

import os
import sys
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *
from grow_replicas_cfg import *
#verify_runnable "global"

log_assert("A zpool mirror/raidz may be increased in capacity by adding a disk.")

log_must([[ZFS,"set","compression=off",TESTPOOL+"/"+TESTFS]])

(out, ret) = cmdExecute([[FILE_WRITE,"-o","create","-f",TESTDIR+"/"+TESTFILE,"-b",BLOCK_SIZE,"-c",WRITE_COUNT,"-d","0"]])

ENOSPC=28
if ret != 28:
   log_fail("file_write completed w/o ENOSPC, aborting!!!")


if not os.path.exists(TESTDIR+"/"+TESTFILE): 
   log_fail(TESTDIR+"/"+TESTFILE +" was not created..")

if not os.path.getsize(TESTDIR+"/"+TESTFILE) > 0 :
   log_fail(TESTDIR+"/"+TESTFILE +" was empty..")

DISK2="/dev/"+sys.argv[1]
DISK3="/dev/"+sys.argv[2]
#

log_must([[ZPOOL,"add","-f",TESTPOOL,POOLTYPE,DISK2,DISK3]])
#        log_must $ZPOOL add -f $TESTPOOL $POOLTYPE $DISK2"s"$SLICE \
#	    $DISK3"s"$SLICE

log_must([[FILE_WRITE,"-o","append","-f",TESTDIR+"/"+TESTFILE,"-b",BLOCK_SIZE,"-c",SMALL_WRITE_COUNT,"-d","0"]])

log_must([[ZFS,"inherit","compression",TESTPOOL+"/"+TESTFS]])
log_pass("TESTPOOL mirror/raidz successfully grown")
