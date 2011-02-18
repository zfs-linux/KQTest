import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_snapshot(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/snapshot/setup.ksh" , disk], env=newenv, cwd=path+"/snapshot")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/snapshot/cleanup.ksh"], env=newenv, cwd=path+"/snapshot")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
	getResources().putHost(self.host)

    def test_snapshot_001_pos(self):
	lib.STFwrap.runScript(self, "/snapshot/snapshot_001_pos.ksh")

    def test_snapshot_002_pos(self):
	lib.STFwrap.runScript(self, "/snapshot/snapshot_002_pos.ksh")

    def test_snapshot_004_pos(self):
        lib.STFwrap.runScript(self, "/snapshot/snapshot_004_pos.ksh")

    def test_snapshot_005_pos(self):
        lib.STFwrap.runScript(self, "/snapshot/snapshot_005_pos.ksh")

    def test_snapshot_006_pos(self):
	lib.STFwrap.runScript(self, "/snapshot/snapshot_006_pos.ksh")

    def test_snapshot_008_pos(self):
	lib.STFwrap.runScript(self, "/snapshot/snapshot_008_pos.ksh")
