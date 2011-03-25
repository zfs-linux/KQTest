import unittest
from lib.KQTest import *
import threading
from lib.utils import *
import lib.STFwrap

class test_scrub_mirror(unittest.TestCase):
    def setUp(self):
        commonSetup(self.id())
        self.cleanup()
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        self.d2 = self.host.getDisk()
        disk0 = self.d1[0].diskname
        disk1 = self.d2[0].diskname
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/scrub_mirror/setup.py" , disk0, disk1], env=newenv, cwd=path+"/scrub_mirror")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def cleanup(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        cmdQuery([path + "/scrub_mirror/cleanup.py"], env=newenv, cwd=path+"/scrub_mirror")

    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/scrub_mirror/cleanup.py"], env=newenv, cwd=path+"/scrub_mirror")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        self.cleanup()
        self.host.putDisk(self.d1)
        self.host.putDisk(self.d2)
        getResources().cleanup()
	getResources().putHost(self.host)

    def test_scrub_mirror_001_pos(self):
	disk = self.d1[0].diskname
	disk = "/dev/" + disk
	lib.STFwrap.runScriptArgs(self, ["/scrub_mirror/scrub_mirror_001_pos.py", disk])

    def test_scrub_mirror_002_pos(self):
	disk = self.d2[0].diskname
	disk = "/dev/" + disk
	lib.STFwrap.runScriptArgs(self, ["/scrub_mirror/scrub_mirror_002_pos.py", disk])

    def test_scrub_mirror_003_pos(self):
	disk = self.d1[0].diskname
	disk = "/dev/" + disk
	lib.STFwrap.runScriptArgs(self, ["/scrub_mirror/scrub_mirror_003_pos.py", disk])

    def test_scrub_mirror_004_pos(self):
	disk = self.d2[0].diskname
	disk = "/dev/" + disk
	lib.STFwrap.runScriptArgs(self, ["/scrub_mirror/scrub_mirror_004_pos.py", disk])
