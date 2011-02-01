#!/usr/bin/python

""" Toplevel script to define the resources available for the test setup
and to run the test cases"""

###########################
## Configuration section ##
###########################

# load zfs test harness configuration settings

ZFS_TH_CONFIG_FILE = 'ZFS.TH.CONFIG'

# read Configuration file to get config data     
try :
    fd = open(ZFS_TH_CONFIG_FILE)
    data = fd.read()
    fd.close()
    sdata = data.split('\n')
    for i in sdata:
        globals()[i.split('=')[0]] = i.split('=')[1]
except :
    print "Error reading config file"

# The device list must be a list not a string of device names

DEVICELIST = DEVICELIST.split()

# done config read
 

###########################
## end of config section ##
###########################

import types
import unittest
from lib.KQTest import *
                              


# set path to build
bu = buildSetup(BUILDROOT, globals())
bu.load()

res = resources(host(map(disk, DEVICELIST)))
loader = unittest.TestLoader()
suite = loader.discover("test", "*.py")
unittest.TextTestRunner(verbosity=2).run(suite)
print "finished"

bu.unload()
