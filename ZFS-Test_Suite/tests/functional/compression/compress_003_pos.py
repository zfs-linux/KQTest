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

import random
################################################################################
#
# __stc_assertion_start
#
# ID: compress_003_pos
#
# DESCRIPTION:
# With 'compression' or 'compress'  set, changing filesystem blocksize cannot 
# cause system panic
#
# STRATEGY:
#	1. Set 'compression' or "compress" to on
#	2. Set different blocksize with ZFS filesystem
#	3. Use 'mkfile' create single block and multi-block files
#	4. Verify the system continued work
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2006-07-26)
#
# __stc_assertion_end
#
################################################################################

def cleanup():
    cmdExecute([[RM,"-f",TESTDIR+"/*"]])


log_assert("Changing blocksize doesn't casue system panic with compression settings")

fs=TESTPOOL+"/"+TESTFS
single_blk_file=TESTDIR+"/singleblkfile."+str(os.getpid())
multi_blk_file=TESTDIR+"/multiblkfile."+str(os.getpid())
blksize=512
fsize=0
offset=0

for propname in ["compression","compress"]:
    for value in get_compress_opts("zfs_compress"):
        print "propname=",propname," value=",value
        log_must([[ZFS,"set",propname+"="+value,fs]])
        
        if value == "gzip-6":
           value="gzip"
                
        real_val = get_prop(propname,fs)

        if real_val != value:
           log_fail("Set property "+propname+"="+value+"== failed.=="+real_val+"==")
        
        blksize = 512

        while blksize <= 131072 : 
              log_must([[ZFS,"set","recordsize="+str(blksize),fs]])
              offset = random.randint(1,131072)
              if offset > blksize: 
                 offset = offset % blksize 
              if (offset % 2) == 0: 
              #keep offset as non-power-of-2
                  offset = offset + 1 
              fsize = offset
              #log_must $MKFILE $fsize $single_blk_file
              log_must([[DD,"if=/dev/zero","of="+single_blk_file,"bs="+str(fsize),"count=1"]])

              fsize = blksize + offset 
              #log_must $MKFILE $fsize $multi_blk_file
              log_must([[DD,"if=/dev/zero","of="+multi_blk_file,"bs="+str(fsize),"count=1"]])
              blksize = blksize * 2 
 
log_pass("The system works as expected while changing blocksize with compression settings")


 
