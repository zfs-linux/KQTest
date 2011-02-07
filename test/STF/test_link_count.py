import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_link_count(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/link_count/setup" , disk], env=newenv, cwd=path+"/link_count")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/link_count/cleanup"], env=newenv, cwd=path+"/link_count")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    @unittest.expectedFailure
    def test_link_count_001(self):
        lib.STFwrap.runScript(self, "/link_count/link_count_001", retcheck=1)        
