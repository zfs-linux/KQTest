import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_truncate(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/truncate/setup" , disk], env=newenv, cwd=path+"/truncate")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/truncate/cleanup"], env=newenv, cwd=path+"/truncate")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    @unittest.expectedFailure
    def test_truncate_001_pos(self):
        lib.STFwrap.runScript(self, "/truncate/truncate_001_pos")
        
    def test_truncate_002_pos(self):
        lib.STFwrap.runScript(self, "/truncate/truncate_002_pos")
