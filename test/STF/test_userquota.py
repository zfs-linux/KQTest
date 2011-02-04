import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_userquota(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
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
        cmdLog(["userdel","quser1"])
        cmdLog(["userdel","quser2"])
        cmdLog(["groupdel","qgroup"])

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/userquota/cleanup"], env=newenv, cwd=path+"/userquota")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    @unittest.expectedFailure
    def test_userquota_001_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_001_pos", retcheck=1)
        
    @unittest.expectedFailure
    def test_userquota_002_pos(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_002_pos", retcheck=1)


    def test_userquota_005_neg(self):
        lib.STFwrap.runScript(self, "/userquota/userquota_005_neg")
