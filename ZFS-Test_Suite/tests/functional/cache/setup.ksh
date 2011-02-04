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
# ident	"@(#)setup.ksh	1.2	09/01/13 SMI"
#

. $STF_SUITE/tests/functional/cache/cache.kshlib
. $STF_SUITE/tests/functional/cache/cache.cfg
. $STF_SUITE/commands.cfg
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/STF/usr/src/tools/stf/contrib/include/logapi.kshlib
. $STF_SUITE/include/libtest.kshlib
#DIRV=`ls / | grep "disk" | tail -n 1`
#DIRV2=`ls / | grep "disk" | head -1`
verify_runnable "global"
verify_runtime $RT_LONG
#if ! verify_cache_support ; then
#	log_unsupported "This system doesn't support cache device"
#fi

#if ! $(is_physical_device $LDEV) ; then
#	log_unsupported "Only physical disk could be cache device"
#fi
#if test -d $DIRV ; then
#	echo "This is if condition"
#	log_must $RM -rf $DIRV
#fi
#if test -d $DIRV2 ; then
#	log_must $RM -rf $DIRV2
#fi
log_must $MKDIR -p $VDIR $VDIR2
dd if=/dev/zero of=$VDIR/a bs=1M count=64
dd if=/dev/zero of=$VDIR/b bs=1M count=64
dd if=/dev/zero of=$VDIR/c bs=1M count=64

dd if=/dev/zero of=$VDIR2/a bs=1M count=64
dd if=/dev/zero of=$VDIR2/b bs=1M count=64
dd if=/dev/zero of=$VDIR2/c bs=1M count=64

log_pass
