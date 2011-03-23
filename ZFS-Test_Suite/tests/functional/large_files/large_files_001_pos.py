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
# ID: large_files_001_pos
#
# DESCRIPTION:
# Write a file to the allowable ZFS fs size.
#
# STRATEGY:
# 1. largest_file will write to a file and increase its size
# to the maximum allowable.
# 2. The last byte of the file should be accessbile without error.
# 3. Writing beyond the maximum file size generates an 'errno' of
# EFBIG.
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



log_assert("Write a file to the allowable ZFS fs size.")

log_note("Invoke 'largest_file' with $TESTDIR/$TESTFILE")
#log_must $LARGEST_FILE $TESTDIR/$TESTFILE

cmdExecute([["./largest_file",TESTDIR+"/"+TESTFILE]])

log_pass("Successfully created a file to the maximum allowable size.")
