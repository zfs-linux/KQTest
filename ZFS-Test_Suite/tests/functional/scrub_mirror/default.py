
import os
import sys
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
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)default.py	1.3	08/08/15 SMI"
#



NUMBER_OF_DISKS=0
DISKS=sys.argv
del DISKS[0]
print DISKS
MIRROR_PRIMARY=""
MIRROR_SECONDARY=""
for i in DISKS:
	if MIRROR_PRIMARY != "":
            MIRROR_SECONDARY=i
	if MIRROR_PRIMARY == "":
            MIRROR_PRIMARY=i

if MIRROR_SECONDARY == "":
	# We need to repartition the single disk to two slices
	SINGLE_DISK=MIRROR_PRIMARY
	MIRROR_SECONDARY=MIRROR_PRIMARY
	SIDE_PRIMARY=SINGLE_DISK +"s0"
	SIDE_SECONDARY=SINGLE_DISK + "s1"
	#Additional
	SIDE_PRIMARY=MIRROR_PRIMARY
	SIDE_SECONDARY=MIRROR_SECONDARY
else:
	SIDE_PRIMARY=MIRROR_PRIMARY + "s0"
	SIDE_SECONDARY=MIRROR_SECONDARY + "s0"
	#Additional
	SIDE_PRIMARY=MIRROR_PRIMARY
	SIDE_SECONDARY=MIRROR_SECONDARY


FILE_COUNT=30
FILE_SIZE=1024 * 1024
MIRROR_MEGS=70
MIRROR_SIZE= str(MIRROR_MEGS) + "m" # default mirror size
DD_BLOCK=64 * 1024
DD_COUNT= MIRROR_MEGS * 1024 * 1024 / DD_BLOCK
FILE_WRITE="../../../bin/file_write"

