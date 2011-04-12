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


################################################################################
#
# __stc_assertion_start
#
# ID: mounttest
#
# DESCRIPTION:
# zfs mount and unmount commands should mount and unmount existing
# file systems.
#
# STRATEGY:
# 1. Call zfs mount command
# 2. Make sure the file systems were mounted
# 3. Call zfs unmount command
# 4. Make sure the file systems were unmounted
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


import os
import sys
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *
from mount_cfg import *


log_note("Mount file systems\n")

for fs in TESTFSS:
    log_must([[ZFS,"mount",fs]])

log_note("Make sure the file systems were mounted\n")

for fs in TESTFSS:
    ret = ismounted(fs)
    if ret != SUCCESS :
       log_fail("File system " + fs +" is not mounted..")

log_note("Unmount the file systems\n")

for fs in TESTFSS:
    log_must([[ZFS,"umount",fs]])

log_note("Make sure the file systems were unmounted\n")

for fs in TESTFSS:
    ret = ismounted(fs)
    if ret == SUCCESS :
       log_fail("File system " + fs +" is mounted..")

log_pass("All file systems are unmounted\n") 
