import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_compression(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/compression/setup.py" , disk], env=newenv, cwd=path+"/compression")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/compression/cleanup.py"], env=newenv, cwd=path+"/compression")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/compression/cleanup.ksh"], env=newenv, cwd=path+"/compression")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.cleanup()
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_compress_001_pos(self):
        lib.STFwrap.runScript(self, "/compression/compress_001_pos.py")
 
    def test_compress_002_pos(self):
        lib.STFwrap.runScript(self, "/compression/compress_002_pos.py")
   
    def test_compress_003_pos(self):
        lib.STFwrap.runScript(self, "/compression/compress_003_pos.ksh")
   
    def test_compress_004_pos(self):
        lib.STFwrap.runScript(self, "/compression/compress_004_pos.ksh")
   
