import random
import unittest
from lib.KQTest import *
import threading
from lib.utils import *
from lib.IOTest import *

class test_stress(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(self.getNumFreeDisks())
        self.tank = self.host.pool("tank", self.d1)
        self.fs = self.tank.getFs()
        

    def tearDown(self):
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_stress(self):
        fs = self.fs
        print "starting stress"
        name = nameGen(fs, "user01").getGen()
        load = loadGen(fs, name, method = ["mmap", "bufferedio"])
        gen = load.getIOTest()
        for i in gen:
            (count, total, test) = i
            print str(count) +"/"+str(total)
            test.run()
            test.verify()
        gen.close()
        name.close()
