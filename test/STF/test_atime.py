import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_reservation(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/atime/setup" , disk], env=newenv, cwd=path+"/atime")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/atime/cleanup"], env=newenv, cwd=path+"/atime")
        self.assertNotIn("ERROR:", stdout, "cleanup failed")
        self.assertNotIn("ERROR:", stderr, "cleanup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_atime_001_pos(self):
        lib.STFwrap.runScript(self, "/atime/atime_001_pos.ksh")

    def test_atime_001_neg(self):
        lib.STFwrap.runScript(self, "/atime/atime_001_neg.ksh")
