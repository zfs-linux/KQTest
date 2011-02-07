import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_no_space(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/no_space/setup.ksh" , disk], env=newenv, cwd=path+"/no_space")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/no_space/cleanup.ksh"], env=newenv, cwd=path+"/no_space")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/no_space/cleanup.ksh"], env=newenv, cwd=path+"/no_space")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_no_space__001_pos(self):
        lib.STFwrap.runScript(self, "/no_space/enospc_001_pos.ksh")
 
