import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_userquota(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/userquota/setup" , disk], env=newenv, cwd=path+"/userquota")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/userquota/cleanup"], env=newenv, cwd=path+"/userquota")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/userquota/cleanup"], env=newenv, cwd=path+"/userquota")
        self.assertNotIn("ERROR:", stdout, "cleanup failed")
        self.assertNotIn("ERROR:", stderr, "cleanup failed")
	self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    @unittest.skip("not ported yet")
    def test_userquota_001_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_001_pos", retcheck=1)
        
    @unittest.skip("not ported yet")
    def test_userquota_002_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_002_pos", retcheck=1)

    @unittest.expectedFailure
    def test_userquota_003_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_003_pos", retcheck=1)

    def test_userquota_005_neg(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_005_neg")

    def test_userquota_006_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_006_pos")

    def test_userquota_007_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_007_pos")

    def test_userquota_008_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_008_pos")

    @unittest.expectedFailure
    def test_userquota_009_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_009_pos", retcheck=1)

    @unittest.expectedFailure
    def test_userquota_010_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_010_pos", retcheck=1)

    @unittest.expectedFailure
    def test_userquota_011_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_011_pos", retcheck=1)

    def test_userquota_012_neg(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_012_neg")

    def test_userspace_001_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userspace_001_pos")

    def test_userspace_002_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userspace_002_pos")

    def test_groupspace_001_pos(self):
        lib.STFwrap.runScript(self, "/userquota/groupspace_001_pos")

    def test_groupspace_002_pos(self):
        lib.STFwrap.runScript(self, "/userquota/groupspace_002_pos")
