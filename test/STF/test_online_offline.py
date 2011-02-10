import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_online_offline(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(2)
	disk = self.d1[0].diskname
        disk = "/dev/" + disk
        disk1 = self.d1[1].diskname
        disk1 = "/dev/" + disk1
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/online_offline/setup.ksh", disk, disk1], env=newenv, cwd=path+"/online_offline")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/online_offline/cleanup.ksh"], env=newenv, cwd=path+"/online_offline")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_online_offline_001_pos(self):
        disk = self.d1[1].diskname
        disk1 = self.d1[0].diskname
        lib.STFwrap.runScriptArgs(self, ["/online_offline/online_offline_001_pos.ksh", disk, disk1])

    def test_online_offline_002_neg(self):
        disk = self.d1[1].diskname
        disk1 = self.d1[0].diskname
        lib.STFwrap.runScriptArgs(self, ["/online_offline/online_offline_002_neg.ksh", disk, disk1])

    def test_online_offline_003_neg(self):
        disk = self.d1[1].diskname
        disk1 = self.d1[0].diskname
        lib.STFwrap.runScriptArgs(self, ["/online_offline/online_offline_003_neg.ksh", disk, disk1])
