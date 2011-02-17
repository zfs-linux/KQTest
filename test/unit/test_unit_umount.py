import random
import unittest
from lib.KQTest import *
import threading
from lib.utils import *
class test_unit_unmount(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        self.tank = self.host.pool("tank", self.d1)
        self.fs = self.tank.getFs()
        self.fsnames =  []
        self.fslist = []
        for i in range(0,10):
            self.fsnames.append("fs"+str(i))
        

    def tearDown(self):
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_unit_unmount(self):
        for i in self.fsnames:
            tmpfs = fs(self.tank, i, self.tank.name+"/"+i)
            ret = tmpfs.create()
            self.assertEqual(ret, 0, "Failed to create file system")
            self.fslist.append(tmpfs)
 
        for i in self.fslist:
            ret = i.unmount()
            self.assertEqual(ret, 0, "Failed to (unit) unmount file system")
