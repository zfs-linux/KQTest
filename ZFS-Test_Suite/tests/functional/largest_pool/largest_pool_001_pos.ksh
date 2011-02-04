#!/bin/ksh -p
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
# ident	"@(#)largest_pool_001_pos.ksh	1.6	09/06/22 SMI"
#
##
#NOTES 
#When we take a volsize in G and less ,at that time largest pool couldn't destroy and it gives a core dumped error.
#That time take a volsize in gb and largest,because on solari its mention as pb,eb etc.
# 

. /home/kqinfo/ZFS-test/ZFS-Test_Suite/include/libtest.kshlib
#. $STF_SUITE/include/libtest.kshlib
. /home/kqinfo/ZFS-test/ZFS-Test_Suite/commands.cfg
#. $STF_SUITE/commands.cfg
. /home/kqinfo/ZFS-test/ZFS-Test_Suite/default.cfg
# . $STF_SUITE/default.cfg
. /home/kqinfo/ZFS-test/ZFS-Test_Suite/include/default_common_varible.kshlib
# . $STF_SUITE/include/default_common_varible.kshlib
. /home/kqinfo/ZFS-test/ZFS-Test_Suite/tests/functional/largest_pool/largest_pool.cfg 
# . $STF_SUITE/tests/functional/largest_pool/largest_pool.cfg


# ##########################################################################
#
# start __stf_assertion__
#
# ASSERTION: largest_pool_001
#
# DESCRIPTION:
#	The largest pool can be created and a dataset in that
#	pool can be created and mounted.
#
# STRATEGY:
#	create a pool which will contain a volume device.
#	create a volume device of desired sizes.
#	create the largest pool allowed using the volume vdev.
#	create and mount a dataset in the largest pool.
#	create some files in the zfs file system.
#	do some zpool list commands and parse the output.
#
# end __stf_assertion__
#
# ##########################################################################

#verify_runnable "global"

#
# Parse the results of zpool & zfs creation with specified size
#
# $1: volume size
#
# return value:
# 0 -> success
# 1 -> failure
#

echo $TESTPOOL
function parse_expected_output
{
	UNITS=`$ECHO $1 | $SED -e 's/^\([0-9].*\)\([a-z].\)/\2/'`
	case "$UNITS" in
		'mb') CHKUNIT="M" ;;
		'gb') CHKUNIT="G" ;;
		'tb') CHKUNIT="T" ;;
		'pb') CHKUNIT="P" ;;
		'eb') CHKUNIT="E" ;;
		*) CHKUNIT="M" ;;
	esac

	log_note "Detect zpool $TESTPOOL in this test machine."
	log_must eval "$ZPOOL list $TESTPOOL > /tmp/j.$$"
	log_must eval "$GREP $TESTPOOL /tmp/j.$$ | \
		$AWK '{print $2}' | $GREP $CHKUNIT"
	
	log_note "Detect the file system in this test machine."
	log_must eval "$DF -F zfs -h > /tmp/j.$$"
	log_must eval "$GREP $TESTPOOL /tmp/j.$$ | \
		$AWK '{print $2}' | $GREP $CHKUNIT"

	return 0
}

#
# Check and destroy zfs, volume & zpool remove the temporary files
#

function cleanup
{

         	log_note "Start cleanup the zfs and pool and vol"
                log_note "Destroy zfs, volume & zpool"
                log_must $ZFS destroy -r $TESTPOOL2/$TESTVOL
        
        $RM -f /tmp/j.* > /dev/null
}

#log_assert "The largest pool can be created and a dataset in that" \
#
#
#pool can be created and mounted."

# Set trigger. When the test case exit, cleanup is executed.

# -----------------------------------------------------------------------
# volume sizes with unit designations.
#
# Note: specifying the number '1' as size will not give the correct
# units for 'df'.  It must be greater than one.
# -----------------------------------------------------------------------
typeset str
typeset -i ret
echo "$VOLSIZES $TESTPOOL2 $1"

for volsize in $VOLSIZES; do
	log_note "volsize=$volsize"
	log_note "Create a pool which will contain a volume device"
    
        create_pool $TESTPOOL2 $1    
      	log_note "Create a volume device of desired sizes: $volsize"
	str=$($ZFS create -sV $volsize $TESTPOOL2/$TESTVOL 2>&1)
	ret=$?
	if (( ret != 0 )); then
		if [[ $($ISAINFO -b) == 32 && \
			$str == *${VOL_LIMIT_KEYWORD1}* || \
			$str == *${VOL_LIMIT_KEYWORD2}* || \
			$str == *${VOL_LIMIT_KEYWORD3}* ]]
		then
			log_unsupported \
				"Max volume size is 1TB on 32-bit systems."
		else
			log_fail "$ZFS create -sV $volsize $TESTPOOL2/$TESTVOL"
		fi
	fi

	log_note "Create the largest pool allowed using the volume vdev"
	create_pool $TESTPOOL "$VOL_PATH"
	log_note "Create a zfs file system in the largest pool"
	log_must $ZFS create $TESTPOOL/$TESTFS
	log_note "Parse the execution result"
	parse_expected_output $volsize

	log_onexit cleanup

	log_note "unmount this zfs file system $TESTPOOL/$TESTFS"
	log_must $ZFS umount $TESTPOOL/$TESTFS

	log_note "Destroy zfs, volume & zpool"
	$ZFS destroy $TESTPOOL/$TESTFS
        echo $TESTPOOL
        umount $TESTPOOL
        zpool destroy -f $TESTPOOL
        echo $TESTPOOL2
	zpool list
        $ZFS destroy -r  $TESTPOOL2/$TESTVOL
        umount $TESTPOOL2
        $ZPOOL destroy $TESTPOOL2
        

       
done
log_onexit cleanup
log_pass "Dateset can be created, mounted & destroy in largest pool succeeded."



