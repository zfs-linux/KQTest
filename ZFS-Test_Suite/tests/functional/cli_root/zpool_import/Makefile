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
# ident	"@(#)Makefile	1.7	07/10/09 SMI"
#

STF_ROOT_CONFIGURE=
STF_USER_CONFIGURE=

STF_ROOT_SETUP=setup
STF_USER_SETUP=

STF_ROOT_CLEANUP=cleanup
STF_USER_CLEANUP=

STF_ROOT_TESTCASES=zpool_import_001_pos zpool_import_002_pos \
    zpool_import_003_pos zpool_import_004_pos zpool_import_005_pos \
    zpool_import_006_pos zpool_import_007_pos zpool_import_008_pos \
    zpool_import_009_neg zpool_import_010_pos zpool_import_011_neg \
    zpool_import_012_pos zpool_import_013_neg \
    zpool_import_rename_001_pos zpool_import_all_001_pos \
    zpool_import_missing_001_pos zpool_import_missing_002_pos \
    zpool_import_missing_003_pos
STF_USER_TESTCASES=

STF_ENVFILES=zpool_import.cfg
STF_INCLUDES=

STF_DONTBUILDMODES=true

include ${STF_TOOLS}/Makefiles/Makefile.master
