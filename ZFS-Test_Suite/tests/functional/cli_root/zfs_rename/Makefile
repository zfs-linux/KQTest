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
# ident	"@(#)Makefile	1.5	09/05/19 SMI"
#

STF_ROOT_CONFIGURE=
STF_USER_CONFIGURE=

STF_ROOT_SETUP=setup
STF_USER_SETUP=

STF_ROOT_CLEANUP=cleanup
STF_USER_CLEANUP=

STF_ROOT_TESTCASES=zfs_rename_001_pos zfs_rename_002_pos \
	zfs_rename_003_pos zfs_rename_004_neg zfs_rename_005_neg \
	zfs_rename_006_pos zfs_rename_007_pos zfs_rename_008_pos \
	zfs_rename_009_neg zfs_rename_010_neg zfs_rename_011_pos \
	zfs_rename_012_neg zfs_rename_013_pos

STF_USER_TESTCASES=

STF_ENVFILES=zfs_rename.cfg
STF_INCLUDES=zfs_rename.kshlib

STF_DONTBUILDMODES=true

include ${STF_TOOLS}/Makefiles/Makefile.master
