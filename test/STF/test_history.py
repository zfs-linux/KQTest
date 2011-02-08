import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_history(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/history/setup.ksh" , disk], env=newenv, cwd=path+"/history")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/history/cleanup.ksh"], env=newenv, cwd=path+"/history")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
	getResources().putHost(self.host)

    def test_history_001_pos(self):
	lib.STFwrap.runScript(self, "/history/history_001_pos.ksh")

    def test_history_003_pos(self):
	lib.STFwrap.runScript(self, "/history/history_003_pos.ksh")

    def test_history_005_neg(self):
	lib.STFwrap.runScript(self, "/history/history_005_neg.ksh")

    def test_history_007_pos(self):
	lib.STFwrap.runScript(self, "/history/history_007_pos.ksh")

