import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_slog(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        disk = self.d1[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/slog/setup" , disk], env=newenv, cwd=path+"/slog")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/slog/cleanup"], env=newenv, cwd=path+"/slog")
        self.assertNotIn("ERROR:", stdout, "cleanup failed")
        self.assertNotIn("ERROR:", stderr, "cleanup failed")
        self.assertEqual(ret, 0, "cleaup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_slog_001_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_001_pos")

    def test_slog_002_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_002_pos")

    def test_slog_003_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_003_pos")

    def test_slog_004_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_004_pos")

    def test_slog_005_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_005_pos")

    def test_slog_006_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_006_pos")

    def test_slog_007_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_007_pos")

    def test_slog_008_neg(self):
        lib.STFwrap.runScript(self, "/slog/slog_008_neg")

    def test_slog_009_neg(self):
        lib.STFwrap.runScript(self, "/slog/slog_009_neg")

    def test_slog_010_neg(self):
        lib.STFwrap.runScript(self, "/slog/slog_010_neg")

    def test_slog_011_neg(self):
        lib.STFwrap.runScript(self, "/slog/slog_011_neg")

    def test_slog_012_neg(self):
        lib.STFwrap.runScript(self, "/slog/slog_012_neg")

    def test_slog_013_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_013_pos")

    def test_slog_014_pos(self):
        lib.STFwrap.runScript(self, "/slog/slog_014_pos")

