import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_cachefile_pool(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(2)
        disk = self.d1[0].diskname
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()

    def tearDown(self):
        self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

 
    def test_cachefile_001_pos(self):
        disk = self.d1[0].diskname
     	disk = "/dev/" + disk
     	disk1 = self.d1[1].diskname
     	disk1 = "/dev/" + disk1
        lib.STFwrap.runScriptArgs(self, ["/cachefile/cachefile_001_pos.ksh", disk, disk1])

    def test_cachefile_002_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
     	disk1 = self.d1[1].diskname
        disk1 = "/dev/" + disk1
        lib.STFwrap.runScriptArgs(self, ["/cachefile/cachefile_002_pos.ksh", disk, disk1])

    def test_cachefile_004_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
	disk1 = self.d1[1].diskname
        disk1 = "/dev/" + disk1
        lib.STFwrap.runScriptArgs(self, ["/cachefile/cachefile_004_pos.ksh", disk, disk1])
   
