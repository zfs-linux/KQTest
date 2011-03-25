import os
import sys
import array
sys.path.append(".")
from default import *
sys.path.append("../../../../lib")
from libtest import *
from logapi import *
from common_variable import *

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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"clean_mirror_common.py	1.4	07/10/09 SMI"
#

# Most of the code related to the clearing of mirrors is duplicated in all
# the test cases below this directory, barring a few minor changes
# involving the device to be affected and the 'object' to use to mangle
# the contents of the mirror.
# This code is sourced into each of these test cases.


def overwrite_verify_mirror(POOL,AFFECTED_DEVICE,OVERWRITING_DEVICE):
    atfile = 0
    files=[]
    cksums=[]
    ewcksum=[]
    while atfile < FILE_COUNT:
        files.append(TESTDIR + "/file." + str(atfile))
        log_must([[FILE_WRITE,"-o","create","-f",TESTDIR+"/file."+str(atfile),"-b",str(FILE_SIZE),"-c","1"]]) 
        cksums.append(cmdExecute([[CKSUM,files[atfile]]])) 
        atfile=atfile+1

    log_must([[DD,"if="+OVERWRITING_DEVICE,"of="+AFFECTED_DEVICE,"seek=8","bs="+str(DD_BLOCK),"count="+str(DD_COUNT),"conv=notrunc"]])

    log_must([[ZPOOL,"scrub",POOL]])
    
    scrubbed="false"
    while scrubbed != "true":
        (out,ret) = cmdExecute([[ZPOOL,"status",POOL],[GREP,"-s","scrub"],[GREP,"-i","repaired"]])
        if ret == 0:
            scrubbed="true"

    afile = 0
    files=[]
    newcksum=[]
    failedcount = 0
    while atfile < FILE_COUNT:
        files.append(TESTDIR + "/file."+str(atfile))
        newcksum.append(cmdExecute([[CKSUM,files[atfile]]])) 
        if newcksum != cksums[atfile]:
            failedcount=failedcount+1
        cmdExecute([[RM,"-f",files[atfile]]]) 
        atfile=atfile+1
        
    if failedcount > 0:
        log_fail("of the "+FILE_COUNT+" files "+failedcount+" did not have the same checksum before and after.")


    


