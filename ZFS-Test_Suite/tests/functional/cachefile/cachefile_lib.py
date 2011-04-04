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
# ident	"@(#)cachefile.kshlib	1.1	08/02/29 SMI"
#


import os
import sys
sys.path.append(".")
from cachefile import *
sys.path.append("../../../../lib")
from libtest import *
from common_variable import *

#
# A function to determine if a given pool name has an entry in cachefile
# returns 1 if the pool is not in the cache, 0 otherwise.

def pool_in_cache(name, file = "") : 

	# checking for the pool name in the strings output of
	# the given cachefile, default is /etc/zfs/zpool.cache

	cachefile = file	
	if len(file) == 0 :
		cachefile = CPATH

	poolname = name

	(RESULT, ret) = cmdExecute([[STRINGS, cachefile],[GREP, "-w", poolname]])
	if  RESULT == "" :
		log_note("pool is not in the cache")
		return 1
	log_note("pool is in the cache")
	return 0

