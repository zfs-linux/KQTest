import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_replacement(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(2)
	disk = self.d1[0].diskname
        disk = "/dev/" + disk
        disk1 = self.d1[1].diskname
        disk1 = "/dev/" + disk1
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/replacement/setup.ksh", disk, disk1], env=newenv, cwd=path+"/replacement")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/replacement/cleanup.py"], env=newenv, cwd=path+"/replacement")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_replacement_001_pos(self):
        lib.STFwrap.runScriptArgs(self, ["/replacement/replacement_001_pos.ksh"])

    def test_replacement_002_pos(self):
        lib.STFwrap.runScriptArgs(self, ["/replacement/replacement_002_pos.ksh"])

    def test_replacement_003_pos(self):
        lib.STFwrap.runScriptArgs(self, ["/replacement/replacement_003_pos.ksh"])

