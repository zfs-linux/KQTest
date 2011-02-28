import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_poolversion(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/poolversion/setup.ksh"], env=newenv, cwd=path+"/poolversion")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/poolversion/cleanup.ksh"], env=newenv, cwd=path+"/poolversion")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        getResources().cleanup()
	getResources().putHost(self.host)

    def test_poolversion_001_pos(self):
	lib.STFwrap.runScript(self, "/poolversion/poolversion_001_pos.ksh")

    def test_poolversion_002_pos(self):
        lib.STFwrap.runScript(self, "/poolversion/poolversion_002_pos.ksh")

