import random
import unittest
from lib.KQTest import *
import threading
from lib.utils import *
from lib.IOTest import *
import time

class test_stress(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk(self.host.getNumFreeDisks())
        self.tank = self.host.pool("tank", self.d1)
        self.fs = self.tank.getFs()
        

    def tearDown(self):
        getResources().cleanup()
        getResources().putHost(self.host)

    def test_stress(self):
        fs = self.fs
        name = nameGen(fs, "user01").getGen()
        load = loadGen(fs, name, method = ["mmap", "bufferedio"])
        gen = load.getIOTest()
        while True:
            i = gen.next()
            (count, total, test) = i
            if threading.active_count() > int(THREADS):
                time.sleep(1)
                continue
            if int(RUN_ONLY) != 0 and count > int(RUN_ONLY):
                break
            print str(count) +"/"+str(total) +"          \r",
            for thrds in  threading.enumerate():
                if not thrds.is_alive():
                    thrds.join()
                if thrds.retval == -1:
                    printLog("Stress-failed cmd: " + thrds.cmdrun())
                    raise Exception("stress failed")
            test.start()

        while threading.active_count() != 1:
            time.sleep(1)
        gen.close()
        name.close()
import threading

class testthr(threading.Thread):
    def run(self):
        print("in test dir")
