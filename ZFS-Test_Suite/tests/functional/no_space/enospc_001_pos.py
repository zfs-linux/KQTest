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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)enospc_001_pos.ksh	1.2	07/01/09 SMI"
# 

import os
import sys
sys.path.append("../../../../lib/")
from libtest import *
from common_variable import *
from logapi import *
from enospc_cfg import *

log_assert ("ENOSPC is returned when file system is full.")
log_must ([[ZFS,"set","compression=off", TESTPOOL+"/"+TESTFS]])

log_note("Writing file: $TESTFILE0 until ENOSPC.")
(out, ret) = cmdExecute ([["./file_write", "-o", "create", "-f", TESTDIR+"/"+TESTFILE0, "-b", BLOCKSZ, "-c", NUM_WRITES, "-d", DATA]])

if str(ret) != ENOSPC:
    log_fail("$TESTFILE0 returned:" + str(ret) + "rather than ENOSPC.")

log_note ("Write another file: $TESTFILE1 but expect ENOSPC.")
(out, ret) = cmdExecute ([["./file_write", "-o", "create", "-f", TESTDIR+"/"+TESTFILE1, "-b", BLOCKSZ, "-c", NUM_WRITES, "-d", DATA]]) 

if str(ret) != ENOSPC:
    log_fail("$TESTFILE0 returned:"+ str(ret) +" rather than ENOSPC.")

log_pass("ENOSPC returned as expected.")



