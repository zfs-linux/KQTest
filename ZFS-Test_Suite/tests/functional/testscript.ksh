#!/bin/ksh

. ${ZFS_TOOLS}/commands.cfg
. ${ZFS_TOOLS}/include/libtest.kshlib
. ${STF_TOOLS}/contrib/include/logapi.kshlib

#log_must ismounted /rohan
#log_must ismounted tank

#log_must mounted tank zfs

#log_must mounted rohan zfs

KEEP="nothing"
NO_POOLS="nothing"

TESTPOOL="tank"
TESTDIR="/mnt"
TESTFS="zfs"

default_setup /dev/sdb
#create_snapshot "tank/zfs" "snap4"
#create_clone "tank/zfs@snap4" "tank/clone4"
 
#destroy_clone "tank/clone4"
#destroy_snapshot "tank/zfs@snap4"

get_prop "mountpoint" "tank"
#default_cleanup
log_assert "hello this is for testing"

log_note " note"

#log_neg ls -l

#log_must ls -l

#log_mustnot ls -l

#log_mustnot_expect 0 ls -l

#log_pos ls -l

log_pass "hello"

