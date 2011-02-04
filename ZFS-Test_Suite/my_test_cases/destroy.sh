#! /bin/ksh
#
# Script for destroying pool


umount /tank/zfs1
umount /tank

rm -rf /tank


/sbin/zpool destroy -f tank 
