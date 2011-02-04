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
# ident	"@(#)Makefile	1.8	09/06/22 SMI"
#

STF_USER_CONFIGURE=
STF_ROOT_CONFIGURE=

STF_ROOT_SETUP=setup
STF_USER_SETUP=

STF_ROOT_CLEANUP=cleanup
STF_USER_CLEANUP=

STF_ROOT_TESTCASES=mountpoint_001_pos mountpoint_002_pos mountpoint_003_pos \
    checksum_001_pos compression_001_pos onoffs_001_pos zfs_set_001_neg \
    reservation_001_neg ro_props_001_pos \
    snapdir_001_pos property_alias_001_pos \
    user_property_001_pos user_property_002_pos \
    user_property_003_neg user_property_004_pos \
    canmount_001_pos canmount_002_pos canmount_003_pos canmount_004_pos \
    version_001_neg zfs_set_002_neg \
    zfs_set_003_neg share_mount_001_neg \
    cache_001_pos cache_002_neg \
    readonly_001_pos

STF_USER_TESTCASES=

STF_ENVFILES=zfs_set.cfg
STF_INCLUDES=zfs_set_common.kshlib

STF_DONTBUILDMODES=true

include $(STF_TOOLS)/Makefiles/Makefile.master
