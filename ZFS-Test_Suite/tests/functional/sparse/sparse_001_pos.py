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
# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)sparse_001_pos.ksh	1.3	09/01/12 SMI"
# 

import os
import sys
sys.path.append("../../../../lib")
from libtest import *
from logapi import *
from common_variable import *
from sparse_cfg import *

################################################################################
#
# __stc_assertion_start
#
# ID: sparse_001_pos
#
# DESCRIPTION:
# Holes in ZFS files work correctly.
#
# STRATEGY:
# 1. Open file
# 2. Write random blocks in random places
# 3. Read each block back to check for correctness.
# 4. Repeat steps 2 and 3 lots of times
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2005-07-04)
#
# __stc_assertion_end
#
################################################################################ 

def cleanup():
    log_must([[RM, "-rf", TESTDIR+"/*"]])

log_assert("Ensure random blocks are read back correctly")

options = ""
options_display = "default options"

log_onexit(cleanup)

if len(HOLES_FILESIZE) != 0:
    options = options +" -f "+ HOLES_FILESIZE

if len(HOLES_BLKSIZE) != 0:
    options = options +" -b "+ HOLES_BLKSIZE

if len(HOLES_COUNT) != 0:
    options = options +" -c "+ HOLES_COUNT

if len(HOLES_SEED) != 0:
    options = options +" -s "+ HOLES_SEED

if len(HOLES_FILEOFFSET) != 0:
    options = options +" -o "+ HOLES_FILEOFFSET

options = options+" -r"
print "options are"+ options + TESTDIR +"/"+ TESTFILE

if len(options) !=0:
    options_display = options

log_note("Invoking file_truc with : "+options_display)
log_must([["./file_trunc", options, TESTDIR+"/"+ TESTFILE]])

tmp = sys.argv[1]
dir = get_device_dir(tmp)
#print"**********"+str(dir)
verify_filesys (TESTPOOL, TESTPOOL+"/"+TESTFS, dir)

log_pass("Random blokcs have been read back correctly")
