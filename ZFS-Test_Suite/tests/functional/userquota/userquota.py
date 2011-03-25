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
import os
import sys
sys.path.append("../../../../lib")
from common_variable import *


#
# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)userquota.py	1.1	09/06/22 SMI"
#

QUSER1="quser1"
QUSER2="quser2"

QGROUP="qgroup"
QGROUP1="qgroup1"
QGROUP1="qgroup2"

UQUOTA_SIZE=1000000
GQUOTA_SIZE=4000000

QFS=TESTPOOL+"/"+TESTFS
QFILE=TESTDIR+"/qfile"
OFILE=TESTDIR+"/ofile"

SNAP_QUOTA=str(100) + "m"
TEST_QUOTA=88888

