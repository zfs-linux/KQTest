import random
import unittest
from lib.KQTest import *
import threading
from lib.utils import *
class test_atime_pos(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        self.tank = self.host.pool("tank", self.d1)
        self.fs = self.tank.getFs()
        

    def tearDown(self):
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_atime_01(self):
        mntpt = self.fs.mntpt
        testfile = mntpt +"newfile"
        touch(testfile)
        before = stat(testfile)
        snap = self.fs.snapshot("snap")
        cat(testfile)
        after = stat(testfile)
        self.assertNotEqual(before.st_atime, after.st_atime, "atime did not change for file access")
        snapfile = snap.mntpt +"newfile"
        printLog("debug: "+snapfile)
        print snapfile 
        print str(snap)
        before = stat(snapfile)
        cat(snapfile)
        aftersnap = stat(snapfile)
        self.assertEqual(before.st_atime, aftersnap.st_atime, "atime changed for on snapshot file")
