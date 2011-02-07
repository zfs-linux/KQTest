import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_grow_pool(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(2)
	disk = self.d1[0].diskname
	(newenv, path) = lib.STFwrap.setupEnv()
	(ret, stdout, stderr) = cmdQuery([path + "/grow_pool/setup.ksh" , disk], env=newenv, cwd=path+"/grow_pool")
	self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/grow_pool/cleanup.ksh"], env=newenv, cwd=path+"/grow_pool")
    

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/grow_pool/cleanup.ksh"], env=newenv, cwd=path+"/grow_pool")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)
 
    def test_grow_pool_001_pos(self):
        disk = self.d1[1].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/grow_pool/grow_pool_001_pos.ksh", disk])
