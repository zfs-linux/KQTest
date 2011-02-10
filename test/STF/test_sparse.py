import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_sparse(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/sparse/setup.ksh", disk], env=newenv, cwd=path+"/sparse")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/sparse/cleanup.ksh"], env=newenv, cwd=path+"/sparse")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/sparse/cleanup.ksh"], env=newenv, cwd=path+"/sparse")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_sparse_001_pos(self):
        lib.STFwrap.runScript(self, "/sparse/sparse_001_pos.ksh")
 
