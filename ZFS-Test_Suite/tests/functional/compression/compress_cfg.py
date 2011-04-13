##!/usr/bin/python
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
# ident	"@(#)compress.cfg	1.4	08/08/15 SMI"
#

import os
import sys

sys.path.append("../../../../lib")
PATH = os.getcwd()

PATH = PATH.rpartition("tests")
FILE_WRITE = PATH[0] + "/bin/file_write"

TESTCTR="testctr"
TESTFILE0="testfile0."+str(os.getpid())
TESTFILE1="testfile1."+str(os.getpid())

RANDFREE_FILE="./randfree_file"
BLOCKSZ="8192"
NUM_WRITES="65536"
DATA="13"
#export STF_TIMEOUT=1200
#export MKFILE=dd

