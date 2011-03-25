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
# ID: poolversion_002_pos
#
# DESCRIPTION:
#
# zpool set version can only increment pool version
#
# STRATEGY:
# 1. Set a version 1 pool to be a version 6 pool
# 2. Verify it's set to version 6
# 3. Attempt to set prior versions
# 4. Verify it's still set to version 6
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2007-07-27)
#
# __stc_assertion_end
#
################################################################################

import sys
sys.path.append("../../../../lib")
from libtest import *


log_assert("zpool set version can only increment pool version")

(TESTPOOL2, ret) = cmdExecute([[ZPOOL,"list"],["cut","-d", ' ',"-f1"],["head","-3"],["tail","-1"]])
TESTPOOL2 = re.sub('\n',"",TESTPOOL2)

log_must([[ZPOOL,"set","version=6",TESTPOOL2]])

# verify it's actually that version - by checking the version property
# and also by trying to set bootfs (which should fail if it is not version 6)

(VERSION, ret) = cmdExecute([[ZPOOL,"get","version",TESTPOOL2],[GREP,"version"],[AWK,'{print $3}']])
VERSION = re.sub('\n',"",VERSION)

if VERSION != "6":
   log_fail("Version "+VERSION+" set for "+TESTPOOL2+" expected version 6!")

log_must([[ZPOOL,"set","bootfs="+TESTPOOL2,TESTPOOL2]])

# now verify we can't downgrade the version
log_mustnot([[ZPOOL,"set","version=5",TESTPOOL2]])
log_mustnot([[ZPOOL,"set","version=-1",TESTPOOL2]])

# verify the version is still 6
(VERSION, ret) = cmdExecute([[ZPOOL,"get","version",TESTPOOL2],[GREP,"version"],[AWK,'{print $3}']])
VERSION = re.sub('\n',"",VERSION)

if VERSION != "6":
   log_fail("Version "+VERSION+" set for "+TESTPOOL2+" expected version 6!")

log_pass("zpool set version can only increment pool version")
