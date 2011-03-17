import sys
import os


from logapi import *
from common_variable import *
from all_commands import *

def default_setup_noexit(disk_l):
   if poolexists(TESTPOOL) == 0:
      print "pool exist",TESTPOOL
      destroy_pool(TESTPOOL)
   else: 
      print "pool does not exist" 
 #  print "TESTPOOL",TESTPOOL
   log_must([[ZPOOL,"create","-f",TESTPOOL,disk_l]])
   log_must([[ZFS,"create",TESTPOOL+"/"+TESTFS]])
   return 0 


def poolexists(testpool):
   if testpool == "":
	sys.exit("\nNo pool name given\n")
   else:
	(data, ret) = cmdExecute([[ZPOOL,"list","-H",testpool]])
	return ret

def destroy_pool(pool):
	if pool == "":
	  sys.exit("\nNo pool name given\n")
        if poolexists(pool) == 0:
          umount_pool_filesystem(pool)
          log_must([[ZPOOL,"destroy","-f",pool]])
        return 0

def umount_pool_filesystem(pool):
	(file_system_mount, ret)  = cmdExecute([["cat","/proc/mounts"],["grep","-F",pool],["cut","-d"," ","-f","2"]])
	file_system_mount = file_system_mount.split('\n')
        file_system_mount.remove("")
        no_of_file_system_mount = len(file_system_mount)
        i = no_of_file_system_mount - 1
        while i >= 0:
          log_must([[UMOUNT,file_system_mount[i]]])
          i = i-1
        return 0	
          
def ismounted(testfs):
        if testfs[0] == '/':
           (file_system_mount, ret) = cmdExecute([[ZFS,"mount"],[AWK,"{print $2}"]])
        else:
          (file_system_mount, ret) = cmdExecute([[ZFS,"mount"],[AWK,"{print $1}"]])
      #  print "ret",ret,"file_system_mount",file_system_mount
	file_system_mount = file_system_mount.split('\n')
        file_system_mount.remove("")
        no_of_file_system_mount = len(file_system_mount)
        i = no_of_file_system_mount - 1
        while i >= 0:
          print "file=",file_system_mount[i],"testfs",testfs
          if file_system_mount[i] == testfs:
            return 0
          i = i-1
        return 1
                      
           
