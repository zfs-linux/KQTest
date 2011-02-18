import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_rename_dirs(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/rename_dirs/setup.ksh" , disk], env=newenv, cwd=path+"/rename_dirs")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/rename_dirs/cleanup.ksh"], env=newenv, cwd=path+"/rename_dirs")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
	getResources().putHost(self.host)

    def test_rename_dirs_001_pos(self):
	lib.STFwrap.runScript(self, "/rename_dirs/rename_dirs_001_pos.ksh")
