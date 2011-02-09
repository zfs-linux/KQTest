import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_grow_replicas(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(4)
	disk = self.d1[0].diskname
        disk = "/dev/" + disk
        disk1 = self.d1[1].diskname
        disk1 = "/dev/" + disk1
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/grow_replicas/setup.ksh", disk, disk1], env=newenv, cwd=path+"/grow_replicas")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/grow_replicas/cleanup.ksh"], env=newenv, cwd=path+"/grow_replicas")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_grow_replicas_001_pos(self):
        disk2 = self.d1[2].diskname
        disk3 = self.d1[3].diskname
        lib.STFwrap.runScriptArgs(self, ["/grow_replicas/grow_replicas_001_pos.ksh", disk2, disk3])

