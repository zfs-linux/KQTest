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
# ident	"@(#)setup.ksh	1.1	07/10/09 SMI"
#

. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/default.cfg
. $STF_SUITE/commands.cfg
. $STF_TOOLS/contrib/include/logapi.kshlib
#verify_runnable "global"

$ZPOOL set 2>&1 | $GREP version > /dev/null
if [ $? -eq 1 ]
then
	log_unsupported "zpool version property not supported on this system."
fi

# create a version 1 pool
#log_must $MKFILE 64m /tmp/zpool_version_1.dat
log_must dd if=/dev/zero of=$1 bs=2M count=32
#log_must $ZPOOL create -o version=1 $TESTPOOL /tmp/zpool_version_1.dat
log_must $ZPOOL create -o version=1 $TESTPOOL $1


# create another version 1 pool
#log_must $MKFILE 64m /tmp/zpool2_version_1.dat
log_must dd if=/dev/zero of=$2 bs=2M count=32
#log_must $ZPOOL create -o version=1 $TESTPOOL2 /tmp/zpool2_version_1.dat
log_must $ZPOOL create -o version=1 $TESTPOOL2 $2

log_pass
