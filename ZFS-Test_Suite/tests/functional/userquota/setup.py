#!/usr/bin/python

#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)setup.py	1.5	09/01/13 SMI"
#

import os
import sys
sys.path.append(".")
from userquota import *
sys.path.append("../../../../lib")
from logapi import *
from libtest import *
from common_variable import *

if not os.geteuid()==0:
	sys.exit("\nOnly root can run this script\n")

if len(sys.argv) not in [2] :
	sys.exit("USAGE: ./setup disk")


if add_group(QGROUP) == 1:
    print "ERROR:can not add group"


print " add_group done "

if add_user(QGROUP,QUSER1) == 1:
    print "ERROR:can not add user"+QUSER1
    
print " add_user 1 done "
if add_user(QGROUP,QUSER2) == 1:
    print "ERROR:can not add user"+QUSER2
    
print " add_user 2 done "

#DISK=${DISKS%% *}
#DISK=$1
DISK=sys.argv
default_setup(DISK[1])
