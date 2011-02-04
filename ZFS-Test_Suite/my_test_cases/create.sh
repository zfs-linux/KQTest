#!/bin/ksh
#
# Script for creating pool and file System


cd /home/kqinfo/ZFS_kq/zfs-0.4.7/scripts/

./zfs.sh


/sbin/zpool create tank -f /dev/sdb1

/sbin/zfs create tank/zfs1
