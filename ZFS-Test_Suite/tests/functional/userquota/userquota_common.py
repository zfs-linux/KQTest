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
# ident	"@(#)userquota_common.kshlib	1.1	09/06/22 SMI"
#

import os
import sys
import array
sys.path.append(".")
from userquota import *
sys.path.append("../../../../lib")
from libtest import *
from logapi import *
from common_variable import *


#
# Check if the test box support userquota or not.
#
def is_userquota_supported():
    if fs_prop_exist("userquota@...") != 0:
        return 1
    return 0


#
# recovery the directory permission for $QFS
#
def recovery_writable(fs):
	mntp = get_prop(mountpoint,fs)
	log_must([[CHMOD,str(0777),mntp]])


#
# reset the userquota and groupquota and delete temporary files
#
def cleanup_quota():
    if datasetexists(QFS):
        log_must([[ZFS,"set","userquota@"+QUSER1+"=none",QFS]])
        log_must([[ZFS,"set","userquota@"+QUSER2+"=none",QFS]])
        log_must([[ZFS,"set","groupquota@"+QGROUP+"=none",QFS]])
        recovery_writable(QFS)
    if os.path.exists(QFILE):
        log_must([[RM,"-f",QFILE]])
    if os.path.exists(OFILE):
        log_must([[RM,"-f",OFILE]])
    return 0



#
# delete user and group that created during the test
# 
def clean_user_group():
        usrlist = [QUSER1,QUSER2]
	for usr in usrlist:
		del_user(usr)
	del_group(QGROUP)
	return 0



#
# run command as specific user
#
def user_run(user,command):
        (group,ret)=cmdExecute([[GROUPS,user]])
	ret = log_must([[SU,user,"-c"] + command])
	print "dd done"
	return ret




#
#  make the $QFS's mountpoint writable for all users
#
def mkmount_writable(fs):
	mntp=get_prop("mountpoint",fs)
	print "mntp=" + mntp
	log_must([[CHMOD,str(0777),mntp]])




