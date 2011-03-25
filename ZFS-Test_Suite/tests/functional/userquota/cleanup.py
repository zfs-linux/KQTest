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

import os
import sys
sys.path.append(".")
from userquota import *
from userquota_common import *
sys.path.append("../../../../lib")
from logapi import *
from libtest import *
from common_variable import *


#
# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)cleanup.py	1.2	09/08/06 SMI"
#
ret = 0
ret  = cleanup_quota()
if ret != 0:
    print "ERROR: cleanup_quota()"
else:
    print "SUCCESS: cleanup_quota()"

#typeset mntp=$(get_prop mountpoint $QFS)
#log_must $CHMOD 0755 $mntp
log_must([[USERDEL,QUSER1]])
log_must([[USERDEL,QUSER2]])
log_must([[GROUPDEL,QGROUP]])
ret = default_cleanup()
if ret != 0:
    print "ERROR: default_cleanup()"
else:
    print "SUCCESS: default_cleanup()"


