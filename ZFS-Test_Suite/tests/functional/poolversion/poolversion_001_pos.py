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


# ident	"@(#)poolversion_001_pos.ksh	1.2	09/01/12 SMI"
#

################################################################################
#
# __stc_assertion_start
#
# ID: poolversion_001_pos
#
# DESCRIPTION:
#
# zpool set version can upgrade a pool

#
# STRATEGY:
# 1. Taking a version 1 pool
# 2. For all known versions, set the version of the pool using zpool set
# 3. Verify that pools version
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

import os
import sys
sys.path.append("../../../../lib")
from libtest import *
from logapi import *
from common_variable import *


log_assert("zpool set version can upgrade a pool")

for version in ["1","2","3","4","5","6","7","8"]:
    log_must([[ZPOOL,"set","version="+str(version),TESTPOOL]])
   
    (set_version, ret) = cmdExecute([[ZPOOL,"get","version",TESTPOOL],[GREP,"version"],[AWK,'{print $3}']])
    set_version = re.sub('\n',"",set_version)
   
   
    if set_version != version :
       log_fail(str(set_version)+" version set for "+TESTPOOL+", expected version "+str(version))
    
log_pass("zpool set version can upgrade a pool")
