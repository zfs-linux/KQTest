""" This module abstracts the typical commonly used functions and
    structure in a filesystem test suite"""

import subprocess
import unittest
import threading
import os

#####
## Globals used in this modules
#####

# the location of the build dir so that we use the correct commands
buildDir = None    

# list of modules that need to be loaded
moduleLoadList = ["/spl/module/spl/spl.ko", "/spl/module/splat/splat.ko", "/zfs/module/avl/zavl.ko",
              "/zfs/module/nvpair/znvpair.ko", "/zfs/module/unicode/zunicode.ko",
              "/zfs/module/zcommon/zcommon.ko", "/zfs/module/zfs/zfs.ko", "/lzfs/module/lzfs.ko"]

# while unloading you don't need the entire path name just the module name
moduleUnloadList = ["lzfs", "zfs", "zunicode", "zcommon", "zavl", "znvpair", "splat", "spl"]

# per Thread local store
threadLocal = threading.local()


# Global Anchor for all the resources
allResources = None

# zpool and zfs command path
# by default assume it is in the path in standard system location
cmdzpool = "zpool"
cmdzfs   = "zfs"

# devnull file for all our commands
devnull = open("/dev/null","rw")

# list of commands used by STF
cmdlist = {"awk":"AWK",
           "arp":"ARP",
           "basename":"BASENAME",
           "cat":"CAT",
           "chgrp":"CHGRP",
           "chmod":"CHMOD",
           "chown":"CHOWN",
           "cksum":"CKSUM",
           "cmp":"CMP",
           "uncompress":"UNCOMPRESS",
           "cp":"CP",
           }
           

#####
## Global helper functions
#####

# Get the infomation about all our resources
def getResources():
    if globals()["allResources"] is None: 
        raise Exception("Resources Not Initialized")
    return allResources


def unmountAll():
    ret = subprocess.call([cmdzfs, "umount", "-a"], stdin=devnull, \
                              stdout=devnull,stderr=devnull)
    if ret != 0:
        raise Exception("Failed to unmount")

def commonSetup(logid):
    threadLocal.testId = logid
    threadLocal.logfile = LOGDIR+"/"+logid
    open(threadLocal.logfile, 'w') # truncate file TODO do properly
    threadLocal.logfd = open(threadLocal.logfile, 'a')
    subprocess.call(["dmesg","-c"], stdout=devnull,stderr=devnull)

def printLog(msg):
    if len(msg) != 0 and msg[-1] != '\n':
        msg +="\n"
    threadLocal.logfd.write(msg)
    threadLocal.logfd.flush()

def cmdQuery(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, dmesg=True):
    logfd = threadLocal.logfd
    stdin = devnull
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    printLog(" ".join(args) +"\n")
    proc = subprocess.Popen(args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags)
    (stdout, stderr) = proc.communicate()
    printLog(stdout)
    printLog(stderr)
    printLog("ret: "+str(proc.returncode)+"\n")
    return (proc.returncode, stdout, stderr)

def cmdLog(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, dmesg=True):
    stdin=devnull
    logfd = threadLocal.logfd
    stdout=logfd
    stderr=logfd
    printLog(" ".join(args) +"\n")
    ret = subprocess.call(args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags)
    printLog("ret: "+str(ret)+"\n")
    if dmesg and DMESG=="True":
        printLog("======= dmesg start ======\n")
        cmdLog(["dmesg","-c"], dmesg=False)
        printLog("======= dmesg end ======\n")
    return ret
        
class disk():
    """This is an abstaraction for a disk"""

    def __init__(self, disk):
        """ A String signifying the disk names we can supply to zpool
        create """
        self.diskname = disk
        self.host = None
        

class mirror(disk):
    "two disking being mirrored"
    pass

class raidz(disk):
    "raidz config of disks"
    pass

# Get the infomation about all our resources
def getResources():
    if globals()["allResources"] is None: 
        raise Exception("Resources Not Initialized")
    return allResources


class resources():
    """ Aggregate all resource available during testing. Including
    remote resources"""
    hosts = []
    hostUsed = []
    hostFree = []
    def __init__(self, newhost):
        if isinstance(newhost, host):
            self.__class__.hosts.append(newhost)
            self.__class__.hostFree.append(newhost)
        else:
            raise Exception(newhost)
        if "allResources" not in globals():
            globals()["allResources"] = self
        globals()["allResources"] = self

    def cleanup(self):
        li = list(self.__class__.hostUsed)
        li.reverse()
        for i in li:
            i.cleanup()
        
    def getHost(self):
        e = self.__class__.hostFree.pop()
        self.__class__.hostUsed.append(e)
        return e 

    def putHost(self, e):
        if not e.checkFree():
            print e.debug()
            raise Exception("Host resources still in use")

        if e in resources.hostUsed:
            self.__class__.hostUsed.remove(e)
            self.__class__.hostFree.append(e)
        else:
            self.debug(self)
            raise Exception(e)
        
    def debug(self):
        print "Debugging Resource"
        print resources.hostFree
        print resources.hosts


class host():
    """Aggregate all resources needs for test here. These could be
    1. disks
    2. nfs/cifs clients 
    3. network ip"""
    def __init__(self, dlist):
        if not isinstance(dlist,list):
            raise Exception("Must me list of disks")
        self.disklist = list(dlist)  # never modify this use diskfree
        self.ip = None
        self.nfs = None
        self.samba = None
        self.diskused = []    # tracks currently used disks
        self.diskfree = list(dlist) # tracks currently free disks
        self.poollist = []
        alldisks=self.getDisk(self.getNumFreeDisks())
        pool = self.pool("clear", alldisks, force=True)
        unmountAll()
        self.putDisk(pool.destroy())

    # destroy pools
    def __del__(self):
        for i in self.poolist:
            if i.created:
                 i.destroy()

    def cleanup(self):
        li = list(self.poollist)
        li.reverse()
        for i in li:
            i.cleanup()
            li = i.destroy()
            self.putDisk(li)

    # Get number of disks
    def getNumFreeDisks(self):
        return len(self.diskfree)


    # Get free disk for use in the host    
    def getDisk(self, num=1):
        ret = []
        for i in range(num):
            e = self.diskfree.pop()
            self.diskused.append(e)
            ret.append(e)
        return ret
            
    # Release disk list once we are done with it
    def putDisk(self, li):
        for d in li:
            if (d in self.disklist) and (d in self.diskused):
                self.diskfree.append(d)
                self.diskused.remove(d)
            else:
                self.debug()
                raise Exception("Invalid disk")
            
    def debug(self):
        print "Printing disk "
        print "disklist " 
        print self.disklist
        print "diskused " 
        print self.diskused
        print "diskfree " 
        print self.diskfree
        print "poollist"
        print self.poollist
    
    # check all host resources have been freed
    def checkFree(self):
        if not (self.poollist == [] and self.diskused == []):
            return False
        else:
            return True

    # Create a pool
    def pool(self, name,  dlist, force=False):
        tank = zpool(self, name, dlist)
        tank.create(force)
        return tank
        
    def pooladd(self, pool):
        self.poollist.append(pool)
        
    def pooldel(self, pool):
        if pool in self.poollist:
            self.poollist.remove(pool)
        else:
            raise Exception("Pool not in list")

        
class zpool():
    """A zpool resource"""
    def __init__(self, chost, name, dlist):
        "initialize a new pool"
        if not isinstance(chost, host):
            raise Exception("Incorrect host")
        self.host = chost
        self.disklist = list(dlist)
        self.created = False
        self.fslist = []
        self.name = name
        self.mountpoint = "/"+name
        self.poolfs = False # should be of type fs

    def __del__(self):
        self.destroy()

    def cleanup(self):
        li = list(self.fslist)
        li.reverse()
        for i in li:
            i.unmount()
            i.destroy()
        
    def getFs(self):
        return self.poolfs 

    # create a the pool 
    def create(self, force=False):
        dl = []
        options = []
        if force:
            options.append("-f")
        for i in self.disklist:
            dl.append(i.diskname)
        # TODO store the stdout and stderr for output in case of error
#        ret = subprocess.call([cmdzpool, "create"]+options+[self.name]+dl, stdin=devnull, stdout=devnull,stderr=devnull)
        ret = cmdLog([cmdzpool, "create"]+options+[self.name]+dl, stdin=devnull, stdout=devnull,stderr=devnull)
        if ret != 0:
            raise Exception("Failed to create pool")
        self.created = True
        self.host.pooladd(self)
        self.poolfs = fs(self, self.name, self.mountpoint, isPool=True)
        return self.poolfs
        

    def destroy(self):
        if not self.created:
            raise Exception("Pool not created can't destroy")
        if len(self.fslist) > 0:
            raise Exception("Children exist" + self.fslist[0].name)

        # TODO store the stdout and stderr for output in case of error
        ret = cmdLog([cmdzpool, "destroy", self.name], stdin=devnull, \
                                  stdout=devnull,stderr=devnull)
        # ret = subprocess.call([cmdzpool, "destroy", self.name], stdin=devnull, \
        #                           stdout=devnull,stderr=devnull)
        if ret != 0:
            raise Exception("Failed to create pool")
        self.created = False
        self.host.pooldel(self)
        # TODO must handle mirror later
        return self.disklist


        
class fs():
    "A filesystem"
    def __init__(self, pool, name, mntpt, isPool=False, snap=False, clone=False, mounted=True):
       self.pool = pool # pool containing this fs
       if mntpt[-1] != "/":
           mntpt = str(mntpt)+"/"
       self.mntpt = mntpt # where it is mounted
       self.name = name
       self.snap = snap
       self.clone = clone
       self.mounted = True
       self.isPool = pool # if this is the pool
       if not isPool:
           pool.fslist.append(self)


    def destroy(self):
        if not self.isPool:
            ret = cmdLog([cmdzfs, "destroy", self.name])
        self.pool.fslist.remove(self)
        return 0

    def mount(self):
        cmdLog([cmdzfs, "mount", self.name])
        if ret != 0:
            raise Exception("can't destroy fs")

    def unmount(self):
        if self.snap:
            cmdLog(["umount",self.mntpt])
        else:
            cmdLog([cmdzfs, "unmount", self.name])


    def snapshot(self, name):
        ret = cmdLog([cmdzfs, "snapshot", self.name + "@" + name])
        if ret != 0:
            raise Exception("can't create snapshot")
        #mount the snapshot
        ret = cmdLog(["ls", self.mntpt +".zfs/snapshot/"+name])
        if ret != 0:
            raise Exception("can't mount snapshot")
        return fs(self.pool, self.name + "@" + name, self.mntpt +".zfs/snapshot/"+name, snap=True)
        
    def create(self):
        pass


class zvol():
    "A zvol"
    pass


class cmds():
    "primitives to invoke the correct commands"
    buildpath = None
    def __init__(self, path):
        cmds.buildpath = path


    
class buildSetup():
    "subroutines to load unload modules, and check them"
    def __init__(self, buildpath, glob):
        # copy the config globals set in the main file
        for i in glob.keys():
            globals()[i] = glob[i]
        commonSetup("resources-setup")
        self.unloadAlways = True # load-unload modules after each test
                                 # to check for leaks
        # make sure we pick up the correct commands
        if buildpath == None :
            globals()["buildDir"] = ""
        else:
            globals()["buildDir"] = buildpath
            cmdzpool = buildpath + "/zfs/cmd/zpool/zpool"
            cmdzfs = buildpath + "/zfs/cmd/zfs/zfs"
        # generate the command.cfg file for STF
        cmdcfg = open(KQTest+"/ZFS-Test_Suite/commands.cfg", "w")
        for i in cmdlist.keys():
            stdout = subprocess.PIPE
            proc = subprocess.Popen(["which", i], stdout=stdout,stderr=devnull)
            (stdout, stderr) = proc.communicate()
            stdout = stdout.split('\n')[0]
            if proc.returncode == 0:
                cmdcfg.write("export "+cmdlist[i] +"="+ stdout+"\n")
            else:
                raise Exception("command " + i + " not found, please install")
        cmdcfg.write("export CMDS=\"\
$AWK $ARP $BASENAME $CAT $CD $CHGRP $CHMOD $CHOWN $CKSUM $CLRI $CMP $COMPRESS \
 $UNCOMPRESS $COREADM $CP $CPIO $CUT $DATE $DD $DEVFSADM $DF $DIFF $DIRCMP \
 $DIRNAME $DU $DUMPADM $ECHO $EGREP $ENV $FDISK $FF $FGREP $FILE $FIND $FMADM \
 $FMDUMP $FORMAT $FSCK $FSDB $FSIRAND $FSTYP $ID $ISAINFO $ISCSIADM $ISCSITADM \
 $GETENT $GREP $GROUPS $GROUPADD $GROUPDEL $GROUPMOD $HEAD $HOSTNAME $KILL $KSH \
 $LABELIT $LOCKFS $LOFIADM $LS $LOGNAME $MDB $METACLEAR $METADB $METAINIT \
 $METASTAT $MKDIR $MKFILE $MKNOD $MODINFO $MODUNLOAD $MOUNT $MV $NCHECK $NEWFS \
 $NAWK $PACK $PAGESIZE $PAX $PING $PRINTF $PFEXEC $PGREP $PKGINFO $PKILL $PS \
 $PSRINFO $PWD $QUOTAON $RCP $REBOOT $RM $RMDIR $RSH $RUNAT $SED $SHARE $SLEEP \
 $SU $SUM $SVCS $SVCADM $SWAP $SWAPADD $SORT $STRINGS $SYNC $TAR $TAIL $TOUCH \
 $TR $TRUE $TUNEFS $UFSDUMP $UFSRESTORE $UMASK $UMOUNT $UNAME $UNIQ $UNSHARE \
 $UNPACK $USERADD $USERDEL $USERMOD $WAIT $WC $ZONEADM $ZONECFG $ZLOGIN \
 $ZONENAME $ZDB $RUNWATTR $ZFS $ZPOOL\"\
")
        
    
    def load(self):
        self.unload(False)
        subprocess.call(["modprobe", "zlib_deflate"])
        res = map(subprocess.call, map((lambda x:["insmod", buildDir+x ]), moduleLoadList))
        if len(res) != res.count(0):
            raise Exception("insmod of zfs modules failed")

    def unload(self, check = True):
        if check:
            res = map(subprocess.call, map((lambda x:["rmmod", x]), moduleUnloadList))
        else:
            res = map((lambda x:subprocess.call(x,stdin=None, stdout=devnull, stderr=devnull)), \
                           map((lambda x:["rmmod", x]), moduleUnloadList))
        if check and (len(res) != res.count(0)):
            raise Exception("error unloading zfs modules")
        

