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
# ident	"@(#)setup.ksh	1.2	07/01/09 SMI"
#


. $STF_SUITE/commands.cfg
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/STF/usr/src/tools/stf/contrib/include/logapi.kshlib

verify_runtime $RT_MEDIUM

DISK=$1

if [ $(id -u) != 0 ]; then
    echo "You must run as root"
fi

if [ $# != 1 ]; then
    echo "USAGE : setup.ksh <Diskname>"
    exit 1
fi

default_setup $DISK

#default_setup_noexit $DISK
#
# Set compression=off to make sure the data is not compressed for 
# reservation testing.
#
log_must $ZFS set compression=off $TESTPOOL

log_pass
