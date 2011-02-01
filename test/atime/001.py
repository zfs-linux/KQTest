import random
import unittest
from lib.KQTest import *
import threading

class atime_pos(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()
        self.tank = self.host.pool("tank", self.d1)
        self.fs = self.tank.getFs()
        

    def tearDown(self):
        unmountAll()
        self.tank.destroy()
        self.host.putDisk(self.d1)
        getResources().putHost(self.host)

    def atime-01(self):
        
