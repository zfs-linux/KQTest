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

import sys
sys.path.append("../../../../lib")
from libtest import *



(out, ret) = cmdExecute_on_stderr([[ZPOOL,"set"],[GREP,"version"]])

if ret != 0:
 log_unsupported("zpool version property not supported on this system.")

TESTPOOL2="tank2"

log_must([[ZPOOL,"destroy",TESTPOOL]])
log_must([[ZPOOL,"destroy",TESTPOOL2]])

log_must([[RM,"/tmp/zpool_version_1.dat"]])
log_must([[RM,"/tmp/zpool_version_2.dat"]])

default_cleanup()
