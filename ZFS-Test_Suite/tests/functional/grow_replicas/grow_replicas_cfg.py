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
# ident	"@(#)grow_replicas.cfg	1.4	08/11/03 SMI"
#
import sys
import os
import random

index = random.randint(1,10) % 2

if index == 0 : 
   POOLTYPE="mirror"
else :
   POOLTYPE="raidz"

BLOCK_SIZE="8192"

#
# Do not make SIZE too large as the three slices may exceed
# the size of the disk, and also slow down the test
# which involves filling until ENOSPC
#
SIZE="100mb"

SMALL_WRITE_COUNT="10000"
#TESTFILE1=file$$.1
WRITE_COUNT="65536000"
TESTFILE="file"+str(os.getpid())+".1"
FILE_WRITE="../../../bin/file_write"
