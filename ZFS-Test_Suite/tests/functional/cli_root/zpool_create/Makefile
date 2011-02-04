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

STF_ROOT_TESTCASES=zpool_create_001_pos zpool_create_002_pos \
		zpool_create_003_pos zpool_create_004_pos \
		zpool_create_005_pos zpool_create_006_pos \
		zpool_create_007_neg \
		zpool_create_008_pos \
		zpool_create_009_neg \
		zpool_create_010_neg \
		zpool_create_011_neg \
		zpool_create_012_neg \
		zpool_create_013_neg \
		zpool_create_014_neg \
		zpool_create_015_neg \
		zpool_create_016_pos \
		zpool_create_017_neg \
		zpool_create_018_pos \
		zpool_create_019_pos \
		zpool_create_020_pos \
		zpool_create_021_pos \
		zpool_create_022_pos \
		zpool_create_023_neg
STF_USER_TESTCASES=

STF_ENVFILES=zpool_create.cfg
STF_INCLUDES=zpool_create.kshlib

STF_DONTBUILDMODES=true

include ${STF_TOOLS}/Makefiles/Makefile.master
