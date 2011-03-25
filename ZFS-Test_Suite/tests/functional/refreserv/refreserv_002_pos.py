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
# ident	"@(#)refreserv_002_pos.ksh	1.3	09/05/19 SMI"
#

import os
import sys
sys.path.append(".")
from refreserv import *
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *

#################################################################################
#
# __stc_assertion_start
#
# ID: refreserv_002_pos
#
# DESCRIPTION:
#	Setting full size as refreservation, verify no snapshot can be created.
#
# STRATEGY:
#	1. Setting full size as refreservation on pool
#	2. Verify no snapshot can be created on this pool
#	3. Setting full size as refreservation on filesystem
#	4. Verify no snapshot can be created on it and its subfs
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2007-11-05)
#
# __stc_assertion_end
#
################################################################################


def cleanup():
	log_must([[ZFS, "set", "refreservation=none", TESTPOOL]])
	if datasetexit(TESTPOOL + "@snap") :
		log_must([[ZFS, "destroy", "-f", TESTPOOL + "@snap"]])

        log_must([[ZFS, "destroy", "-rf", TESTPOOL + "/" + TESTFS]])
        log_must([[ZFS, "create",  TESTPOOL + "/" + TESTFS]])
        log_must([[ZFS, "set", "mountpoint" + "=" + TESTDIR, TESTPOOL + "/" + TESTFS]])


log_assert("Setting full size as refreservation, verify no snapshot can be created.")
log_onexit(cleanup)

log_must([[ZFS, "create", TESTPOOL + "/" + TESTFS + "/" + "subfs"]])

datasets=[TESTPOOL + "/" + TESTFS, TESTPOOL + "/" + TESTFS + "/" + "subfs"]

for ds in datasets : 
	#
	# Verify refreservation on dataset
	#
	log_must([[ZFS, "set", "quota=25M", ds]])
	log_must([[ZFS, "set", "refreservation=24M", ds]])
	mntpnt = get_prop("mountpoint", ds)
	log_must([[TOUCH, mntpnt + "/" + TESTFILE]])
	log_mustnot([[ZFS, "snapshot", ds + "@snap." + ds]])
	if datasetexists(ds + "@snap." + ds) == 0 :
		log_fail("ERROR: $ds@snap.$ds should not exists.")
	log_must([[ZFS, "set", "quota=none", ds]])
	log_must([[ZFS, "set", "refreservation=none", ds]])

log_pass("Setting full size as refreservation, verify no snapshot can be created.")
