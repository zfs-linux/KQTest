import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_refreserv(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/refreserv/setup.py" , disk], env=newenv, cwd=path+"/refreserv")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/refreserv/cleanup.py"], env=newenv, cwd=path+"/refreserv")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/refreserv/cleanup.py"], env=newenv, cwd=path+"/refreserv")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_refreserv_001_pos(self):
        lib.STFwrap.runScript(self, "/refreserv/refreserv_001_pos.py")

    def test_refreserv_002_pos(self):
        lib.STFwrap.runScript(self, "/refreserv/refreserv_002_pos.py")
   
    def test_refreserv_003_pos(self):
        lib.STFwrap.runScript(self, "/refreserv/refreserv_003_pos.py")
   
    def test_refreserv_004_pos(self):
        lib.STFwrap.runScript(self, "/refreserv/refreserv_004_pos.py")

    def test_refreserv_005_pos(self):
	lib.STFwrap.runScript(self, "/refreserv/refreserv_005_pos.py")  

