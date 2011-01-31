""" This module abstracts the typical commonly used functions and
    structure in a filesystem test suite"""

import subprocess

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

# Global Anchor for all the resources
allResources = None

# zpool and zfs command path
# by default assume it is in the path in standard system location
cmdzpool = "zpool"
cmdzfs   = "zfs"

# devnull file for all our commands
devnull = open("/dev/null","rw")

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

    # destroy pools
    def __del__(self):
        for i in self.poolist:
            if i.created:
                 i.destroy()

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
    def pool(self, name,  dlist):
        tank = zpool(self, name, dlist)
        tank.create()
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
#        self.fslist = fs()

    def __del__(self):
        self.destroy()
    

    # create a the pool 
    def create(self):
        dl = []
        for i in self.disklist:
            dl.append(i.diskname)
        # TODO store the stdout and stderr for output in case of error
        ret = subprocess.call([cmdzpool, "create"]+[self.name]+dl, stdin=devnull, stdout=devnull,stderr=devnull)
        if ret != 0:
            raise Exception("Failed to create pool")
        self.created = True
        self.host.pooladd(self)

    def destroy(self):
        if not self.created:
            raise Exception("Pool not created can't destroy")
        # TODO store the stdout and stderr for output in case of error
        ret = subprocess.call([cmdzpool, "destroy", self.name], stdin=devnull, \
                                  stdout=devnull,stderr=devnull)
        if ret != 0:
            raise Exception("Failed to create pool")
        self.created = False
        self.host.pooldel(self)
        # TODO must handle mirror later
        return self.disklist

    def unmountAll(self):
        ret = subprocess.call([cmdzfs, "umount", "-a"], stdin=devnull, \
                                  stdout=devnull,stderr=devnull)
        if ret != 0:
            raise Exception("Failed to unmount")
        
class fs():
    "A filesystem"
    def __init__(self, pool, mntpt):
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
    def __init__(self, buildpath):
        self.unloadAlways = True # load-unload modules after each test
                                 # to check for leaks
        # make sure we pick up the correct commands
        if buildpath == None :
            globals()["buildDir"] = ""
        else:
            globals()["buildDir"] = buildpath
            cmdzpool = buildpath + "/zfs/cmd/zpool/zpool"
            cmdzfs = buildpath + "/zfs/cmd/zfs/zfs"

    def load(self):
        self.unload(False)
        res = map(subprocess.call, map((lambda x:["insmod", buildDir+x ]), moduleLoadList))
        if len(res) != res.count(0):
            raise Exception("insmod of zfs modules failed")

    def unload(self, check = True):
        if check:
            res = map(subprocess.call, map((lambda x:["rmmod", buildDir+x]), moduleUnloadList))
        else:
            res = map((lambda x:subprocess.call(x,stdin=None, stdout=devnull, stderr=devnull)), \
                           map((lambda x:["rmmod", buildDir+x]), moduleUnloadList))
        if check and (len(res) != res.count(0)):
            raise Exception("error unloading zfs modules")
        
