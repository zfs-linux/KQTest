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
from grow_replicas_cfg import *

if len(sys.argv) == 3:
   DISK = sys.argv[1]
   DISK1= sys.argv[2]
else:
   sys.exit("\nUsage : Enter the two argument as disk name\n")

log_note("Creating pool type: "+POOLTYPE)


#if [[ -n $DISK2 ]]
#then
#        log_note "No spare disks available. Using slices on $DISK"
#	for i in $SLICE0 $SLICE1 $SLICE3 $SLICE4 ; do
#       	log_must set_partition $i "$cyl" $SIZE $DISK
#		cyl=$(get_endslice $DISK $i)
#	done
#        create_pool $TESTPOOL $POOLTYPE ${DISK}s$SLICE0 \
#	    ${DISK}s$SLICE1
#else
#        log_must set_partition $SLICE "" $SIZE $DISK0
#        log_must set_partition $SLICE "" $SIZE $DISK1
#        create_pool $TESTPOOL $POOLTYPE ${DISK0}s${SLICE} \
#	    ${DISK1}s$SLICE

log_must([[ZPOOL,"create","-f",TESTPOOL,POOLTYPE,DISK,DISK1]])
#fi

(out, ret) = cmdExecute([[RM,"-rf",TESTDIR]])
if ret != 0:
  log_unresolved("Could not remove "+TESTDIR)

(out, ret) = cmdExecute([[MKDIR,"-p",TESTDIR]])
if ret != 0:
  log_unresolved("Could not create "+TESTDIR)


log_must([[ZFS,"create",TESTPOOL+"/"+TESTFS]])
log_must([[ZFS,"set","mountpoint="+TESTDIR,TESTPOOL+"/"+TESTFS]])

log_pass("Setup done successfully")
