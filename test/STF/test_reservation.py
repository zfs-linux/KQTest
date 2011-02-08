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
        (ret, stdout, stderr) = cmdQuery([path + "/reservation/setup.ksh" , disk], env=newenv, cwd=path+"/reservation")
        self.assertEqual(ret, 0, "setup failed")
        self.assertNotIn("ERROR:", stdout, "setup failed")
        self.assertNotIn("ERROR:", stderr, "setup failed")
        
    def tearDown(self):
        (newenv, path) = lib.STFwrap.setupEnv()
        (ret, stdout, stderr) = cmdQuery([path + "/reservation/cleanup.ksh"], env=newenv, cwd=path+"/reservation")
        self.assertNotIn("ERROR:", stdout, "cleanup failed")
        self.assertNotIn("ERROR:", stderr, "cleanup failed")
        self.host.putDisk(self.d1)
        getResources().cleanup()
        getResources().putHost(self.host)

#   def test_userquota_001_pos(self):
#       lib.STFwrap.runScript(self, "/userquota/userquota_001_pos", retcheck=1)
#    @unittest.expectedFailure
#   def test_userquota_010_pos(self):
#       lib.STFwrap.runScript(self, "/userquota/userquota_010_pos", retcheck=1)
#    def test_userquota_012_neg(self):
#       lib.STFwrap.runScript(self, "/userquota/userquota_012_neg")
 
    def test_reservation_001_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_001_pos.ksh")

    def test_reservation_002_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_002_pos.ksh")

    def test_reservation_003_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_003_pos.ksh")

    def test_reservation_004_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_004_pos.ksh")

    def test_reservation_005_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_005_pos.ksh")

    def test_reservation_006_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_006_pos.ksh")

    def test_reservation_007_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_007_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_008_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_008_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_009_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_009_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_010_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_010_pos.ksh")

    def test_reservation_011_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_011_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_012_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_012_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_013_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_013_pos.ksh")

    def test_reservation_014_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_014_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_015_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_015_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_016_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_016_pos.ksh")
        
    @unittest.skip("not ported yet")
    def test_reservation_017_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_017_pos.ksh")

    @unittest.skip("not ported yet")
    def test_reservation_018_pos(self):
        lib.STFwrap.runScript(self, "/reservation/reservation_018_pos.ksh")

 
