import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_cache(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/cache/setup.ksh"], env=newenv, cwd=path+"/cache")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/cache/cleanup.ksh"], env=newenv, cwd=path+"/cache")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    @unittest.expectedFailure("problem with output parsing script")
    def test_cache_001_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_001_pos.ksh", disk])

    @unittest.expectedFailure("problem with output parsing script")
    def test_cache_002_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_002_pos.ksh", disk])

    def test_cache_003_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_003_pos.ksh", disk])

    def test_cache_004_neg(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_004_neg.ksh", disk])

    def test_cache_005_neg(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_005_neg.ksh", disk])

    def test_cache_006_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_006_pos.ksh", disk])

    def test_cache_007_neg(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_007_neg.ksh", disk])

    def test_cache_008_neg(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_008_neg.ksh", disk])

    def test_cache_009_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_009_pos.ksh", disk])

    def test_cache_010_neg(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_010_neg.ksh", disk])

    def test_cache_011_pos(self):
        disk = self.d1[0].diskname
        disk = "/dev/" + disk
        lib.STFwrap.runScriptArgs(self, ["/cache/cache_011_pos.ksh", disk])
