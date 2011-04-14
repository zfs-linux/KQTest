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
from logapi import *
from all_commands import *
from common_variable import *



if not os.geteuid()==0:
        sys.exit("\nOnly root can run this script\n")

if len(sys.argv) not in [2] :
        sys.exit("USAGE: ./setup disk")

DISK=sys.argv
default_setup(DISK[1])
