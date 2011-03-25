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
import sys
sys.path.append("../../../../lib")
from libtest import *
from compress_cfg import *
import random

################################################################################
#
# __stc_assertion_start
#
# ID: compress_004_pos
#
# DESCRIPTION:
# With 'compression' set, a file with non-power-of-2 blocksize storage space 
# can be freed as will normally.
#
# STRATEGY:
#	1. Set 'compression' or 'compress' to on or lzjb
#	2. Set different recordsize with ZFS filesystem
#	3. Repeatedly using 'randfree_file' to create a file and then free its  
#	   storage space with different range, the system should work normally.  
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
    log_must([[RM,"-f",TESTDIR+"/*"]])

def create_free_testing(file_size,file):
    for start in [0,random.randint(1,100000) % file_size]:
        dist = file_size - start
        for len in [random.randint(1,100000) % dist, dist, start + dist]:
            log_must([[RANDFREE_FILE,"-l",str(file_size),"-s",str(start),"-n",str(len),file]])
        if os.path.exists(file):
           log_must([[RM,"-f",file]]) 


log_assert("Creating non-power-of-2 blocksize file and freeing the file storage space at will should work normally with compression setting") 

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
              fsize = random.randint(1,131072)
              if fsize > blksize:
                 fsize = fsize % blksize
              if (fsize % 2) == 0:
              #keep offset as non-power-of-2
                  fsize = fsize + 1
              create_free_testing(fsize,single_blk_file)
              
	      # doing multiple blocks testing
	      avail=get_prop("available",fs)
	      blknum = int(avail) / blksize 
	      # we just test <10 multi-blocks to limit testing time
              blknum = blknum % 9 
              while blknum < 2 : 
                    blknum = blknum + random.randint(1,100000) % 9  
	      if blknum % 2 == 0: 
	         blknum = blknum + 1    # keep blknum as odd
	      fsize = blknum * blksize 
	      create_free_testing(fsize,multi_blk_file)

	      blksize = blksize * 2 

cleanup()
log_pass("Creating and freeing non-power-of-2 blocksize file work as expected.")
