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
# ident	"@(#)cachefile_004_pos.ksh	1.2	09/06/22 SMI"
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

#################################################################################
#
# __stc_assertion_start
#
# ID: cachefile_004_pos
#
# DESCRIPTION:
#	Verify set, export and destroy when cachefile is set on pool.
#
# STRATEGY:
#	1. Create two pools with one same cahcefile1.
#	2. Set cachefile of the two pools to another same cachefile2.
#	3. Verify cachefile1 not exist.
#	4. Export the two pools.
#	5. Verify cachefile2 not exist.
#	6. Import the two pools and set cachefile to cachefile2.
#	7. Destroy the two pools.
#	8. Verify cachefile2 not exist.
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2009-04-24)
#
# __stc_assertion_end
#
################################################################################

DISKS=sys.argv

def cleanup() :
	
	poolname = [ TESTPOOL1, TESTPOOL2 ]

	for name in poolname :
		ret = poolexists(name)
		if ret == 0 :
	 		destroy_pool(name)
		

	mntpnt = get_prop("mountpoint", TESTPOOL)
	i=0
	while i < 2 :
		if os.path.isfile(mntpnt + "/vdev" + str(i)) : 
			log_must([[RM, "-f", mntpnt + "/vdev" + str(i)]])
		i = i + 1	
	ret =  poolexists(TESTPOOL)
	if ret == 0 :	
		destroy_pool(TESTPOOL)

	path = [ CPATH1, CPATH2 ]
	
	for file in path :
		if os.path.isfile(file) :
			log_must([[RM,file]])



log_assert("Verify set, export and destroy when cachefile is set on pool.")
log_onexit(cleanup)

log_must([[ZPOOL, "create", TESTPOOL,DISKS[1]]])

mntpnt =  get_prop("mountpoint", TESTPOOL)
i=0
while i < 2 :
	log_must([[DD, "if=/dev/zero", "of=" + mntpnt + "/vdev" + str(i), "bs=1M", "count=64"]])
	i = i + 1

vdev = [ mntpnt + "/vdev0", mntpnt + "/vdev1" ]

log_must([[ZPOOL, "create", "-o", "cachefile=" + CPATH1, TESTPOOL1, vdev[0]]])
ret = pool_in_cache(TESTPOOL1, CPATH1)
if ret != 0 :
	log_pass(" ERROR : pool not in cache")

log_must([[ZPOOL, "create", "-o", "cachefile=" + CPATH1, TESTPOOL2, vdev[1]]])
ret = pool_in_cache(TESTPOOL2, CPATH1)
if ret != 0 :
        log_pass(" ERROR : pool not in cache")

log_must([[ZPOOL, "set", "cachefile=" + CPATH2, TESTPOOL1]])
ret = pool_in_cache(TESTPOOL1, CPATH2)
if ret != 0 :
        log_pass(" ERROR : pool not in cache")

log_must([[ZPOOL, "set", "cachefile=" + CPATH2, TESTPOOL2]])
ret = pool_in_cache(TESTPOOL2, CPATH2)
if ret != 0 :
        log_pass(" ERROR : pool not in cache")

if os.path.isfile(CPATH1) :
	log_fail("Verify set when cachefile is set on pool.")

log_must([[ZPOOL, "export", TESTPOOL1]])
log_must([[ZPOOL, "export", TESTPOOL2]])
if os.path.isfile(CPATH2) :
	log_fail("Verify set when cachefile is set on pool.")


log_must([[ZPOOL, "import", "-d", mntpnt, TESTPOOL1]])
log_must([[ZPOOL, "set", "cachefile=" + CPATH2, TESTPOOL1]])
ret = pool_in_cache(TESTPOOL1, CPATH2)
if ret != 0 :
        log_pass(" ERROR : pool not in cache")

log_must([[ZPOOL, "import", "-d", mntpnt, TESTPOOL2]])
log_must([[ZPOOL, "set", "cachefile=" + CPATH2, TESTPOOL2]])
ret = pool_in_cache(TESTPOOL2, CPATH2)
if ret != 0 :
        log_pass(" ERROR : pool not in cache")

log_must([[ZPOOL, "destroy", TESTPOOL1]])
log_must([[ZPOOL, "destroy", TESTPOOL2]])

if os.path.isfile(CPATH2) :
	log_fail("Verify destroy when cachefile is set on pool.")


log_pass([["Verify set, export and destroy when cachefile is set on pool."]])

