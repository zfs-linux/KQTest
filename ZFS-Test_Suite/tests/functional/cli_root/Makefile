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
# ident	"@(#)Makefile	1.6	09/06/22 SMI"
#

STF_ROOT_CONFIGURE=
STF_USER_CONFIGURE=

STF_ROOT_SETUP=
STF_USER_SETUP=

STF_ROOT_CLEANUP=
STF_USER_CLEANUP=

STF_ROOT_TESTCASES=
STF_USER_TESTCASES=

#
# STF_BUILD_SUBDIRS and STF_EXECUTE_SUBDIRS should be
# listed in the order returned by ls(1m)
#
STF_BUILD_SUBDIRS=zdb \
   zfs zfs_send zfs_clone zfs_create zfs_copies zfs_destroy zfs_get \
   zfs_inherit zfs_mount zfs_rename zfs_reservation \
   zfs_receive zfs_rollback zfs_set zfs_share zfs_snapshot \
   zfs_unmount zfs_unshare zfs_promote zfs_upgrade \
   zpool zpool_add zpool_attach zpool_create zpool_clear \
   zpool_destroy zpool_detach zpool_export zpool_import \
   zpool_history zpool_offline zpool_online zpool_replace \
   zpool_scrub zpool_status zpool_upgrade zpool_set zpool_get \
   zpool_remove zpool_expand

STF_EXECUTE_SUBDIRS=zdb \
   zfs zfs_send zfs_clone zfs_create zfs_copies zfs_destroy zfs_get \
   zfs_inherit zfs_mount zfs_rename zfs_reservation \
   zfs_receive zfs_rollback zfs_set zfs_share zfs_snapshot \
   zfs_unmount zfs_unshare zfs_promote zfs_upgrade \
   zpool zpool_add zpool_attach zpool_create zpool_clear \
   zpool_destroy zpool_detach zpool_export zpool_import \
   zpool_history zpool_offline zpool_online zpool_replace \
   zpool_scrub zpool_status zpool_upgrade zpool_set zpool_get \
   zpool_remove zpool_expand

STF_ENVFILES=cli.cfg
STF_INCLUDES=cli_common.kshlib

STF_DONTBUILDMODES=true

include ${STF_TOOLS}/Makefiles/Makefile.master
