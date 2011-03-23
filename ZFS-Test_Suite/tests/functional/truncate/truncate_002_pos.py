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
# ID: truncate_002_pos
#
# DESCRIPTION:
# Tests file truncation within ZFS while a sync operation is in progress.
#
# STRATEGY:
# 1. Copy a file to ZFS filesystem
# 2. Copy /dev/null to same file on ZFS filesystem
# 3. Execute a sync command
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

import sys
sys.path.append("../../../../lib")
from libtest import *
from logapi import *
from common_variable import *


def cleanup():
   if os.path.exists(TESTDIR) == 1:
      log_must([[RM,"-rf",TESTDIR+"/*"]])


log_assert("Ensure zeroed file gets written correctly during a sync operation")

srcfilename="../../../../lib/all_commands.py"


log_note("Copying "+srcfilename+" to "+TESTFILE)
log_must([[CP,srcfilename,TESTDIR+"/"+TESTFILE]])

log_note("Copying /dev/null to "+TESTFILE)
log_must([[CP,"/dev/null",TESTDIR+"/"+TESTFILE]])

log_note("Now 'sync' the filesystem")
#log_must([["cd",TESTDIR]])

os.chdir(TESTDIR)
print "current dir is "+ os.getcwd()
log_must([[SYNC]])

cleanup()
log_pass("Successful truncation within ZFS while a sync operation is in progress.")
