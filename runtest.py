""" Toplevel script to define the resources available for the test setup
and to run the test cases"""

###########################
## Configuration section ##
###########################
# All the test setup specific detail are in this section. you will
# need to modify this for your test to work correctly.

DEVICELIST= ["sda","sdb", "sdc"]
BUILDROOT= "/root/github/"


###########################
## end of config section ##
###########################

import types
import unittest
from lib.KQTest import *

# set path to build
bu = buildSetup(BUILDROOT)
bu.load()

res = resources(host(map(disk, DEVICELIST)))
suite = unittest.TestLoader().discover("test", "*.py", "test")
unittest.TextTestRunner(verbosity=2).run(suite)
print "finished"

bu.unload()
