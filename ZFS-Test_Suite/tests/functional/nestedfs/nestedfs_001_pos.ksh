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
# ident	"@(#)nestedfs_001_pos.ksh	1.2	07/01/09 SMI"
#
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/commands.cfg
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/tests/functional/nestedfs/nestedfs.cfg


################################################################################
#
# __stc_assertion_start
#
# ID: nestedfs_001_pos
#
# DESCRIPTION:
# Given a pool create a nested file system and a ZFS file system
# in the nested file system. Populate the file system.
#
# As a sub-assertion, the test verifies that a nested file system with
# a mounted file system cannot be destroyed.
#
# STRATEGY:
# 1. Create a file in the new mountpoint
# 2. Unmount the new mountpoint
# 3. Show a nested file system with file systems cannot be destroyed
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2005-07-04)
#
# __stc_assertion_end
#
################################################################################

verify_runnable "both"

typeset OP=create
typeset -i BLOCKSZ=8192
typeset -i NUM_WRITES=600
typeset -i DATA=0

log_assert "Verify a nested file system can be created/destroyed."

log_must $FILE_WRITE -o $OP -f $TESTDIR1/$TESTFILE0 \
	 -c $NUM_WRITES -d $DATA
log_note "File creation path $TESTDIR1/$TESTFILE0"
log_note "A nested file system was successfully populated."

log_must $ZFS unmount $TESTDIR

log_note "Verify that a nested file system with a mounted file system "\
    "cannot be destroyed."
log_mustnot $ZFS destroy  $TESTPOOL/$TESTCTR
