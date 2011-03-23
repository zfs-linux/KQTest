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
import time
import os
import sys
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *
from compress_cfg import *

################################################################################
#
# __stc_assertion_start
#
# ID: compress_002_pos
#
# DESCRIPTION:
# Create two files of exactly the same size. One with compression
# and one without. Ensure the compressed file is smaller.
#
#NOTE: This test uses a dataset rather than a simple file system
# STRATEGY:
# Use "zfs set" to turn on compression and create files before
# and after the set call. The compressed file should be smaller.
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





log_assert("Ensure that compressed files in a dataset are smaller.")

log_note("Ensure compression is off")
log_must([[ZFS,"set","compression=off",TESTPOOL+"/"+TESTCTR]])

log_note("Writing file without compression...")
log_must([[FILE_WRITE,"-o","create","-f",TESTDIR1+"/"+TESTFILE0,"-b",BLOCKSZ,"-c",NUM_WRITES,"-d",DATA]])

log_note("Add compression property to the dataset and write another file")
log_must([[ZFS,"set","compression=on",TESTPOOL+"/"+TESTCTR]])

log_must([[FILE_WRITE,"-o","create","-f",TESTDIR1+"/"+TESTFILE1,"-b",BLOCKSZ,"-c",NUM_WRITES,"-d",DATA]])

time.sleep(60)

(FILE0_BLKS, ret) = cmdExecute([[DU,"-k",TESTDIR1+"/"+TESTFILE0],[AWK,'{ print $1}']])
(FILE1_BLKS, ret) = cmdExecute([[DU,"-k",TESTDIR1+"/"+TESTFILE1],[AWK,'{ print $1}']])

print "FILE0_BLKS=",FILE0_BLKS,"   FILE1_BLKS=",FILE1_BLKS

if FILE0_BLKS <= FILE1_BLKS :
   log_fail(TESTFILE0+" is smaller than "+TESTFILE1)

log_pass(TESTFILE0+" is bigger than "+TESTFILE1) 


