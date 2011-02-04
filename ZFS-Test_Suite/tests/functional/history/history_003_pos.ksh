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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)history_003_pos.ksh	1.2	07/01/09 SMI"
#

. $STF_SUITE/commands.cfg
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/tests/functional/history/history_common.kshlib
. ./history.cfg

#################################################################################
#
# __stc_assertion_start
#
# ID: history_003_pos
#
# DESCRIPTION:
#	zpool history can record and output huge log.
#
# STRATEGY:
#	1. Create two 100M virtual disk files.
#	2. Create test pool using the two virtual files.
#	3. Loop 2000 times to set compression to test pool.
#	4. Make sure 'zpool history' output correctly.
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2006-07-05)
#
# __stc_assertion_end
#
################################################################################

verify_runnable "global"

function cleanup
{
	datasetexists $spool && log_must $ZPOOL destroy $spool
	[[ -f $VDEV0 ]] && log_must $RM -f $VDEV0
	[[ -f $VDEV1 ]] && log_must $RM -f $VDEV1
}

log_assert "zpool history limitation test."
log_onexit cleanup

mntpnt=$(get_prop mountpoint $TESTPOOL)
(( $? != 0 )) && log_fail "get_prop mountpoint $TESTPOOL"

VDEV0=$mntpnt/vdev0; VDEV1=$mntpnt/vdev1

log_must $DD if=/dev/zero of=$VDEV0 bs=1M count=100
log_must $DD if=/dev/zero of=$VDEV1 bs=1M count=100

spool=smallpool.$$; sfs=smallfs.$$
log_must $ZPOOL create $spool $VDEV0 $VDEV1
log_must $ZFS create $spool/$sfs

typeset -i orig_count=$($ZPOOL history $spool | $WC -l | $AWK '{print $1}')

typeset -i i=0
while ((i < 400)); do
	$ZFS set compression=off $spool/$sfs
	$ZFS set compression=on $spool/$sfs
	$ZFS set compression=off $spool/$sfs
	$ZFS set compression=on $spool/$sfs
	$ZFS set compression=off $spool/$sfs
	((i += 1))
	echo "$i.."
done

typeset -i entry_count=$($ZPOOL history $spool | $WC -l | $AWK '{print $1}')

if ((entry_count - orig_count != 2000)); then
	log_fail "The entries count error: entry_count=$entry_count " \
		 "orig_count = $orig_count"
fi

log_pass "zpool history limitation test passed."
