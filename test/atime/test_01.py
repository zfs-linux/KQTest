import random
import unittest
from lib.KQTest import *
import threading

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
        snap = self.fs.snapshot("snap")
