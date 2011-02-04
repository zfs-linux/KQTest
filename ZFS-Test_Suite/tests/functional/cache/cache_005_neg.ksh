#!/bin/ksh -p
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
# ident	"@(#)cache_005_neg.ksh	1.2	09/05/19 SMI"
#

. $STF_SUITE/tests/functional/cache/cache.kshlib
. $STF_SUITE/tests/functional/cache/cache.cfg
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/commands.cfg

#################################################################################
#
# __stc_assertion_start
#
# ID: cache_005_neg
#
# DESCRIPTION:
#	Replacing a cache device fails.
#
# STRATEGY:
#	1. Create pool with cache devices.
#	2. Replacing one cache device
#	3. Verify replace fails
#	4. Destroy and loop to create pool with different configuration.
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2008-03-26)
#
# __stc_assertion_end
#
################################################################################
if [[ $# -ne 2 ]];then
	echo "Usage : Two </vdev> disk must"
	exit
fi
verify_runnable "global"
verify_disk_count "$LDEV2"
VDIR=`ls / | grep "disk" | tail -1`
log_assert "Replacing a cache device fails."
log_onexit cleanup

for type in "" "mirror" "raidz" "raidz2"
do
	
	log_must $ZPOOL create -f $TESTPOOL $type /$VDIR/a /$VDIR/b /$VDIR/c \
		cache $1

	sdev=$1
	tdev=$2
	log_mustnot $ZPOOL replace $TESTPOOL $sdev $tdev
	log_mustnot $ZPOOL replace $TESTPOOL $1 $2
	log_must verify_cache_device $TESTPOOL $sdev 'ONLINE'
	log_must check_vdev_state $TESTPOOL $tdev ""
	
	log_must umount $TESTPOOL 
	log_must $ZPOOL destroy -f $TESTPOOL
done

log_pass "Replacing a cache device fails."
