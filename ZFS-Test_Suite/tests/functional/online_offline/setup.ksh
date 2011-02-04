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
# ident	"@(#)setup.ksh	1.3	09/05/19 SMI"
#

echo $STF_TOOLS
echo $STF_SUITE


. $STF_SUITE/commands.cfg
. $STF_SUITE/include/libtest.kshlib
. $STF_SUITE/include/default_common_varible.kshlib
. $STF_TOOLS/contrib/include/logapi.kshlib
. $STF_SUITE/tests/functional/no_space/enospc.cfg

verify_runnable "global"

#verify_disk_count "$DISKS" 2

#echo $RANDOM

#index=`expr $RANDOM % 2`
#case $index in
#0)
	log_note "Pool Type: Mirror"
	#default_mirror_setup $DISKS

	echo $1 $2
	
	default_mirror_setup_noexit $1 $2
#	;;
#1)	log_note "Pool Type: RAID-Z"
#	default_raidz_setup $DISKS
#	;;
#esac

log_pass
