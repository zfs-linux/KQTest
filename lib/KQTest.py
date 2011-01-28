""" This module abstracts the typical commonly used functions and
    structure in a filesystem test suite"""

# the location of the build dir so that we use the correct commands
buildDir = None    

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

class resources():
    """ Aggregate all resource available during testing. Including
    remote resources"""
    hosts = []
    hostUsed = []
    hostFree = []
    def __init__(self, newhost):
        if isinstance(newhost, host):
            resources.hosts.append(newhost)
            resources.hostsFree.append(newhost)
        else:
            raise newhost
        
    def getHost(self):
        e = resources.hostsFree.remove()
        resources.hostUsed.add(e)
        return e

    def putHost(self, e)



class host():
    """Aggregate all resources needs for test here. These could be
    1. disks
    2. nfs/cifs clients 
    3. network ip"""
    def __init__(self, dlist):
        self.disklist = dlist
        self.ip = None
        self.nfs = None
        self.samba = None
        self.diskused = None
        self.diskfree = dlist
        self.poollist = None

class zpool():
    """A zpool resource"""
    def __init__(self, dlist):
        "initialize a new pool"
        self.disklist = dlist

class fs():
    "A filesystem"
    pass

class zvol():
    "A zvol"
    pass


class cmds():
    "primitives to invoke the correct commands"
    buildpath = None
    def __init__(self, path):
        cmds.buildpath = path


    
class kernel():
    "subroutines to load unload modules, and check them"
    def __init__(self, buildpath):
        self.unloadAlways = True # load-unload modules after each test
                                 # to check for leaks
        self.buildDir = buildpath # path to the build directory
        # make sure we pick up the correct commands
        if buildpath == None :
            buildDir = ""
        else:
            buildDir = buildpath
        
        
