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
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_SUITE/include/libtest.kshlib


DISKS=$1

if test $# -ne 1
then
    echo "USAGE : setup.ksh <DiskName>"
    exit 1
fi

if [ $(id -u) != 0 ]; then
         echo "USAGE: You must be run this script as root"
	 exit 1	
fi

$ZPOOL history > /dev/null 2>&1
(($? != 0)) && log_unsupported

DISK=${DISKS%% *}
default_setup $DISK
