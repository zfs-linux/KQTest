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
# ident	"@(#)setup.ksh	1.5	09/06/22 SMI"
#
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/commands.cfg
. $STF_SUITE/tests/functional/grow_replicas/grow_replicas.cfg

#verify_runnable "global"
DISK=$1
DISK1=$2
#if ! $(existent_of_disk $DIS) ; then
#	log_unsupported "This directory cannot be run on raw files."
#fi
log_note "Creating pool type: $POOLTYPE"

if [[ -n $DISK2 ]]; then
        log_note "No spare disks available. Using slices on $DISK"
	for i in $SLICE0 $SLICE1 $SLICE3 $SLICE4 ; do
        	log_must set_partition $i "$cyl" $SIZE $DISK
		cyl=$(get_endslice $DISK $i)
	done
        create_pool $TESTPOOL $POOLTYPE ${DISK}s$SLICE0 \
	    ${DISK}s$SLICE1
else
#        log_must set_partition $SLICE "" $SIZE $DISK0
#        log_must set_partition $SLICE "" $SIZE $DISK1
#        create_pool $TESTPOOL $POOLTYPE ${DISK0}s${SLICE} \
#	    ${DISK1}s$SLICE
	 zpool create  -f  $TESTPOOL $POOLTYPE $DISK $DISK1
fi

$RM -rf $TESTDIR  || log_unresolved Could not remove $TESTDIR
$MKDIR -p $TESTDIR || log_unresolved Could not create $TESTDIR

log_must $ZFS create $TESTPOOL/$TESTFS
log_must $ZFS set mountpoint=$TESTDIR $TESTPOOL/$TESTFS

log_pass
