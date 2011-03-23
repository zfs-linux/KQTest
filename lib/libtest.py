import sys
import os
SUCCESS = 0

from logapi import *
from common_variable import *
from all_commands import *

container = "false"
volume = "false"

def default_setup(disk_l):
   default_setup_noexit(disk_l)

def default_container_setup(disk_l):
    global container     # Needed to modify global copy of container 
    container = "true"
 #   print "container===",container
    default_setup_noexit(disk_l)
 #   print "container=========",container

def default_setup_noexit(disk_l):
   if poolexists(TESTPOOL) == SUCCESS:
      print "pool exist",TESTPOOL
      destroy_pool(TESTPOOL)
   else: 
      print "pool does not exist" 
 #  print "TESTPOOL",TESTPOOL
   log_must([[ZPOOL,"create","-f",TESTPOOL,disk_l]])

   (out, ret) = cmdExecute([[RM,"-rf",TESTDIR]])
   if ret != 0:
      log_unresolved("Could not remove "+TESTDIR)

   (out, ret) = cmdExecute([[MKDIR,"-p",TESTDIR]])
   if ret != 0:
      log_unresolved("Could not create "+TESTDIR)

   log_must([[ZFS,"create",TESTPOOL+"/"+TESTFS]])
#   print "container",container
   if container == "true" :
      
      (out, ret) = cmdExecute([[RM,"-rf",TESTDIR1]])
      if ret != 0:
         log_unresolved("Could not remove "+TESTDIR1)

      (out, ret) = cmdExecute([[MKDIR,"-p",TESTDIR1]])
      if ret != 0:
         log_unresolved("Could not create "+TESTDIR)

      log_must([[ZFS,"create",TESTPOOL+"/"+TESTCTR]])
      log_must([[ZFS,"set","canmount=off",TESTPOOL+"/"+TESTCTR]])
      log_must([[ZFS,"create",TESTPOOL+"/"+TESTCTR+"/"+TESTFS1]])
      log_must([[ZFS,"set","mountpoint="+TESTDIR1,TESTPOOL+"/"+TESTCTR+"/"+TESTFS1]])

      global container
      container = "false"
   return 0 

   

def poolexists(testpool):
   if testpool == "":
	sys.exit("\nERROR : No pool name given\n")
   else:
	(data, ret) = cmdExecute([[ZPOOL,"list","-H",testpool]])
	return ret

def destroy_pool(pool):
	if pool == "":
	  sys.exit("\nERROR : No pool name given\n")
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
        print "ret",ret,"file_system_mount",file_system_mount
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
                      
def existent_of_disk(disk):
       (out, ret) = cmdExecute([["find","/dev/","-name",disk],["grep","-F",disk]])
       if ret != SUCCESS:
         print " Disk not exist.. \n Enter valid Disk name.. " 
         return 1
       else:
         (out, ret) = cmdExecute([["cat","/proc/mounts"],["grep",disk]])  
         if ret == SUCCESS:
            print " Disk is Already mounted "
            return 1
       return 0

def default_cleanup():
        # Destroying the pool will also destroy any
        # filesystems it contains.
	(pool_names, ret) = cmdExecute([[ZPOOL,"list","-H","-o","name"],[GREP,"-v",NO_POOLS]])
	pool_names = pool_names.split('\n')
        pool_names.remove("")
        no_of_pools = len(pool_names)
        print "All Pools : ",pool_names
        i = 0
        # Here, we loop through the pools we're allowed to
        # destroy, only destroying them if it's safe to do
        # so.

        while i < no_of_pools :
          print "Checking Pool ",pool_names[i]
          if safe_to_destroy_pool(pool_names[i]) == SUCCESS :
             print "destroy pool"
	     destroy_pool(pool_names[i])
          i = i + 1
        
        log_must([[ZFS,"mount","-a"]])


            
def safe_to_destroy_pool(pool):
       DONT_DESTROY=""
       ALTMOUNTPOOL=""
        # We check that by deleting the $1 pool, we're not
        # going to pull the rug out from other pools. Do this
        # by looking at all other pools, ensuring that they
        # aren't built from files or zvols contained in this pool.
       (pool_names, ret) = cmdExecute([[ZPOOL,"list","-H","-o","name"]])
       no_of_pools = len(pool_names)
       i = 0 
       while i < no_of_pools :
         (FILEPOOL, ret ) = cmdExecute([[ZPOOL,"status","-v",pool_names[i]],[GREP,"/"+pool+"/"],[AWK,'{print $1}']])
        # this is a list of the top-level directories in each of the files
                # that make up the path to the files the pool is based on

         print "FILEPOOL = ",FILEPOOL
         # this is a list of the zvols that make up the pool
         (ZVOLPOOL, ret ) = cmdExecute([[ZPOOL,"status","-v",pool_names[i]],[GREP,"/dev/zvol/dsk/"+pool+"$"],[AWK,'{print $1}']])
          # also want to determine if it's a file-based pool using an
                # alternate mountpoint...
 
    	 (POOL_FILE_DIRS, ret) = cmdExecute([[ZPOOL,"status","-v",pool_names[i]],[GREP,"/"],[AWK,'{print $1}'],[AWK,"-F/",'{print $2}'],[GREP,"-v","dev"]])
         no_of_pool_file_dirs = len(POOL_FILE_DIRS)
         j = 0
         while j < no_of_pool_file_dirs:
            (out, ret) = cmdExecute([[ZFS,"list","-H","-r","-o","mountpoint",pool],[GREP,pool+"$"],[AWK,'{print $1}']])
            ALTMOUNTPOOL = ALTMOUNTPOOL + out

         if FILEPOOL != "":
           DONT_DESTROY="true"
           log_note("Pool"+pool+"is built from"+FILEPOOL+"on"+pool)
         
         if ZVOLPOOL != "":
           DONT_DESTROY="true"
           log_note("Pool"+pool+"is built from"+ZVOLPOOL+"on"+pool)
         
         if ALTMOUNTPOOL != "":
           DONT_DESTROY="true"
           log_note("Pool"+pool+"is built from"+ALTMOUNTPOOL+"on"+pool)

         if DONT_DESTROY == "":
           log_note("Returning 0 from here")
           return 0
 
         else :
           log_note("Warning: it is not safe to destroy"+pool+"!") 
           return 1      



#
# Given a pair of disks, set up a storage pool and dataset for the mirror
# @parameters: $1 the primary side of the mirror
#   $2 the secondary side of the mirror
# @uses: ZPOOL ZFS TESTPOOL TESTFS
def default_mirror_setup_noexit(SIDE_PRIMARY,SIDE_SECONDARY):
	func="default_mirror_setup_noexit"
	primary=SIDE_PRIMARY
	secondary=SIDE_SECONDARY

        if primary == "":
           log_fail(" "+func+": No parameters passed")
	if secondary == "":
           log_fail(" "+func+": No secondary partition passed")

        if os.path.isdir("/"+TESTPOOL) == True:
           cmdExecute([[RM,"-rm","/"+TESTPOOL]])
           
	log_must([[ZPOOL,"create","-f",TESTPOOL,"mirror",primary,secondary]])
	log_must([[ZFS,"create",TESTPOOL+"/"+TESTFS]])
	log_must([[ZFS,"set","mountpoint="+TESTDIR, TESTPOOL+"/"+TESTFS]])

def default_mirror_setup(SIDE_PRIMARY,SIDE_SECONDARY):
   default_mirror_setup_noexit(SIDE_PRIMARY,SIDE_SECONDARY)
   