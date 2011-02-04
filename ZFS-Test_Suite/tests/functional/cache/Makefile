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
# ident	"@(#)Makefile	1.2	09/01/13 SMI"
#

STF_USER_CONFIGURE=
STF_ROOT_CONFIGURE=

STF_ROOT_SETUP=setup
STF_USER_SETUP=

STF_ROOT_CLEANUP=cleanup
STF_USER_CLEANUP=

STF_ROOT_TESTCASES=cache_001_pos cache_002_pos cache_003_pos cache_004_neg \
	cache_005_neg cache_006_pos cache_007_neg cache_008_neg \
	cache_009_pos cache_010_neg cache_011_pos
STF_USER_TESTCASES=

STF_ENVFILES=cache.cfg
STF_INCLUDES=cache.kshlib

STF_DONTBUILDMODES=true

include $(STF_TOOLS)/Makefiles/Makefile.master
