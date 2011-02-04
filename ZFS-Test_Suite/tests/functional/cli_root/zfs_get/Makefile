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
# ident	"@(#)Makefile	1.4	09/06/22 SMI"
#

STF_USER_CONFIGURE=
STF_ROOT_CONFIGURE=

STF_ROOT_SETUP=setup
STF_USER_SETUP=

STF_ROOT_CLEANUP=cleanup
STF_USER_CLEANUP=

STF_ROOT_TESTCASES=zfs_get_001_pos zfs_get_002_pos \
	zfs_get_003_pos zfs_get_004_pos \
	zfs_get_005_neg zfs_get_006_neg \
	zfs_get_007_neg zfs_get_008_pos \
	zfs_get_009_pos zfs_get_010_neg

STF_USER_TESTCASES=

STF_ENVFILES=zfs_get.cfg
STF_INCLUDES=zfs_get_common.kshlib zfs_get_list_d.kshlib

STF_DONTBUILDMODES=true

include $(STF_TOOLS)/Makefiles/Makefile.master
