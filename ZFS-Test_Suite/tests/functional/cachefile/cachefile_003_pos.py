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
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)cachefile_003_pos.ksh	1.1	08/02/29 SMI"
#

import os
import sys
import re
sys.path.append(".")
from cachefile import *
from cachefile_lib import *
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *

################################################################################
#
# __stc_assertion_start
#
# ID: cachefile_003_pos
#
# DESCRIPTION:
#
# Setting altroot=<path> and cachefile=$CPATH for zpool create is succeed
#
# STRATEGY:
# 1. Attempt to create a pool with -o altroot=<path> -o cachefile=<value>
# 2. Verify the command succeed
#
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2007-09-10)
#
# __stc_assertion_end
#
################################################################################

DISKS = sys.argv

pid = os.getpid()

TESTDIR = "/altdir." + str(pid)

def cleanup() :

	if poolexists(TESTPOOL) :
		destroy_pool(TESTPOOL)

        PATH = [ CPATH1, CPATH2 ]
        for file in PATH :
                if  os.path.isfile(file) :
                        log_must([[RM, file]])

	if os.path.isdir(TESTDIR) :
		log_must([[RMDIR,TESTDIR]])


log_assert("Setting altroot=path and cachefile=$CPATH for zpool create succeed.")
log_onexit(cleanup)

opts = [ "none", "none", CPATH, "-", CPATH1, CPATH1, CPATH2, CPATH2]
i=0

while  i < len(opts) :
 
	log_must([[ZPOOL,"create", "-o", "altroot=" + TESTDIR, "-o", "cachefile=" + opts[i], TESTPOOL, DISKS[1]]])
	if opts[i] != "none" :  
		ret = pool_in_cache(TESTPOOL,opts[i])
		if ret != 0 :
			log_pass(" ERROR : pool not in cache")
	else :
		ret = pool_in_cache(TESTPOOL) 
		if ret != 1 :
			log_pass(" ERROR : pool in cache")

	
	(PROP, ret) = get_pool_prop("cachefile", TESTPOOL)

	PROP = re.sub('\n', "", PROP)

        if PROP != opts[i+1] :
                log_fail("cachefile property not set as expected. Expect: " + str(opts[i+2]) + " Current: " + str(PROP))

	log_must([[ZPOOL, "destroy", TESTPOOL]])
	i = i + 2 

log_pass("Setting altroot=path and cachefile=$CPATH for zpool create succeed.")

