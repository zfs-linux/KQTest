#!/usr/bin/python
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
# ident	"@(#)sparse.cfg	1.3	08/08/15 SMI"
#

import os

pid = os.getpid()

TESTFILE="testfile."+str(pid)
HOLES_FILESIZE= "671088" # 64 Mb
HOLES_BLKSIZE="4096"
HOLES_SEED= "" 
HOLES_FILEOFFSET= ""
HOLES_COUNT= "1630"	   # FILESIZE/BLKSIZE/8
STF_TIMEOUT=3600
