#! /bin/ksh -p
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
# ident	"@(#)reservation_015_pos.ksh	1.4	09/08/06 SMI"
#

. $STF_SUITE/tests/functional/reservation/reservation.kshlib
. $STF_SUITE/commands.cfg
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/STF/usr/src/tools/stf/contrib/include/logapi.kshlib
. $STF_SUITE/tests/functional/reservation/reservation.cfg



###############################################################################
#
# __stc_assertion_start
#
# ID: reservation_015_pos
#
# DESCRIPTION:
#
# In pool with a full filesystem and a regular volume with an implicit 
# reservation, setting the reservation on the volume to 'none' should allow 
# more data to be written to the filesystem.
#
#
# STRATEGY:
# 1) Create a regular non-sparse volume (which implicitly sets the reservation 
#    property to a value equal to the volume size)
# 2) Create a filesystem at the same level
# 3) Fill up the filesystem
# 4) Set the reservation on the volume to 'none'
# 5) Verify can write more data to the filesystem
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2005-07-19)
#
# __stc_assertion_end
#
################################################################################

verify_runnable "global"

log_assert "Setting volume reservation to 'none' allows more data to" \
	" be written to top level filesystem"

function cleanup 
{
	datasetexists $TESTPOOL/$TESTVOL && \
            log_must $ZFS destroy $TESTPOOL/$TESTVOL

        [[ -e $TESTDIR/$TESTFILE1 ]] && \
                log_must $RM -rf $TESTDIR/$TESTFILE1

        [[ -e $TESTDIR/$TESTFILE2 ]] && \
                log_must $RM -rf $TESTDIR/$TESTFILE2

	$ZFS unmount -a > /dev/null 2>&1
	log_must $ZFS mount -a
}

log_onexit cleanup

space_avail=`get_prop available $TESTPOOL`

#
# To make sure this test doesn't take too long to execute on
# large pools, we calculate a volume size which when applied 
# to the volume will ensure we have RESV_FREE_SPACE 
# left free in the pool which we can quickly fill.
#
(( resv_size_set = space_avail - RESV_FREE_SPACE ))
resv_size_set=$(floor_volsize $resv_size_set)

log_must $ZFS create -V $resv_size_set $TESTPOOL/$TESTVOL

space_avail_still=`get_prop available $TESTPOOL`

fill_size=`expr $space_avail_still + $RESV_TOLERANCE`
write_count=`expr $fill_size / $BLOCK_SIZE`

# Now fill up the filesystem (which doesn't have a reservation set
# and thus will use up whatever free space is left in the pool).
log_must ./$FILE_WRITE -o create -f $TESTDIR/$TESTFILE1 -b $BLOCK_SIZE \
        -c $write_count -d 0
ret=$?
if (( $ret != $ENOSPC )); then
	log_fail "Did not get ENOSPC as expected (got $ret)."
fi

if fs_prop_exist refreserv; then
        log_must $ZFS set refreservation=none $TESTPOOL/$TESTVOL
else
	log_must $ZFS set reservation=none $TESTPOOL/$TESTVOL
fi


log_must ./$FILE_WRITE -o create -f $TESTDIR/$TESTFILE2 -b $BLOCK_SIZE \
        -c 1000 -d 0

log_pass "Setting top level volume reservation to 'none' allows more " \
	"data to be written to the top level filesystem"
