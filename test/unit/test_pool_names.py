import random
import string
import unittest
from lib.KQTest import *
import threading
from lib.utils import *
class test_pool_names_pos(unittest.TestCase):

    def setUp(self):
        commonSetup(self.id())
        self.host = getResources().getHost()
        self.d1 = self.host.getDisk()

    def tearDown(self):
	self.host.putDisk(self.d1)
        getResources().putHost(self.host)

    def checkCommandStatus(self, name, retcheck = 0):
        disk = self.d1[0].diskname	
        (ret, stdout, stderr) = cmdQuery(["zpool", "create", name, "-f", disk]) 
	self.assertNotIn("ERROR:", stdout, "got:: " + stdout)
 	self.assertNotIn("ERROR:", stderr, "got:: " + stderr)
 	self.assertEqual(ret, retcheck, "ret: " + str(ret))

	(ret, stdout, stderr) = cmdQuery(["zpool", "destroy", name]) 
	self.assertNotIn("ERROR:", stdout, "got:: " + stdout)
 	self.assertNotIn("ERROR:", stderr, "got:: " + stderr)
 	self.assertEqual(ret, retcheck, "ret: " + str(ret))
 
    def test_pool_names__001_pos(self):
        printLog("Ensure letters of the alphabet are allowable")
        for poolname in string.letters :
           self.checkCommandStatus(poolname)
       
        printLog("Ensure a variety of unusual names passes")
        name = [ "a_", "a-","a:", "a.", "a123456", "bc0t0d0", "m1rr0r_p00l", "ra1dz_p00l", 
        	 "araidz2", "C0t2d0", "cc0t0", "raid2:-_.", "mirr_:-.", "m1rr0r-p00l", "ra1dz-p00l", 
        	 "spar3_p00l", "spar3-p00l", "hiddenmirrorpool", "hiddenraidzpool", "hiddensparepool"]
        for poolname in name :
            self.checkCommandStatus(poolname)

        printLog("Valid pool names were accepted correctly.")


       
    def test_pool_names__002_neg(self):
        printLog("Ensure that a set of invalid names cannot be used to create pools.")
        printLog("Ensure invalid characters fail")
        name = [ "!", "\"", "#", "$", "%", "&", "'", "(", ")", "\*", "+", ",", "-", "\.", "/", "\\",
        	 "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "\?", "@",
        	 "[", "]", "^", "_", "\`", "{", "|", "}", "~" ]
        for poolname in name :
            self.checkCommandStatus(poolname, 1)


        printLog("Check that invalid octal values fail")
        pool = [ "\000", "\001", "\002", "\003", "\004", "\005", "\006", "\007","\010", "\011", "\012",
        	 "\013", "\014", "\015", "\017", "\020", "\021", "\022", "\023", "\024", "\025", "\026"
       	         "\027", "\030", "\031", "\032", "\033", "\034", "\035", "\036", "\037", "\140", "\177" ]
        for poolname in name :
            self.checkCommandStatus(poolname, 1)


        printLog("Verify invalid pool names fail")
        name = [ "sde", "sdb", "sda1", "mirror", "raidz", ",,", ",,,,,,,,,,,,,,,,,,,,,,,,,"
        	 "2222222222222222222", "mirror_pool", "raidz_pool", "mirror-pool", "raidz-pool", 
		 "spare", "spare_pool", "spare-pool", "raidz1-", "raidz2:", ":aaa",  "_ccc", ".ddd" ]
        for poolname in name :
            self.checkCommandStatus(poolname, 1)


        printLog("Invalid names and characters were caught correctly")
        

