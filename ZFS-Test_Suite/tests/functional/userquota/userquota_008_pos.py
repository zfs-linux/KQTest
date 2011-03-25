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
# ident	"@(#)userquota_008_pos.ksh	1.1	09/06/22 SMI"
#

################################################################################
#
# __stc_assertion_start
#
# ID: userquota_008_pos.py
#
# DESCRIPTION:
#       
#      zfs get all <fs> does not print out userquota/groupquota
#
# STRATEGY:
#       1. set userquota and groupquota to a fs
#       2. check zfs get all fs
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING STATUS: COMPLETED (2009-04-16)
#
# __stc_assertion_end
#
###############################################################################


import os
import sys
sys.path.append(".")
from userquota import *
from userquota_common import *
sys.path.append("../../../../lib")
from logapi import *
from libtest import *
from common_variable import *


###############################################################################


def cleanup():
  ret  = cleanup_quota()
  if ret != 0:
      print "ERROR: cleanup_quota()"
  else:
      print "SUCCESS: cleanup_quota()"

log_onexit(cleanup)


log_assert("Check zfs get all will not print out user|group quota")
log_must([[ZFS,"get","userquota@"+QUSER1+"=50m",QFS]])
log_must([[ZFS,"get","groupquota@"+QGROUP+"=100m",QFS]])

log_mustnot([[ZFS,"get","all",QFS],[GREP,"userquota"]])
log_mustnot([[ZFS,"get","all",QFS],[GREP,"groupquota"]])

log_pass("zfs get all will not print out user|group quota")

