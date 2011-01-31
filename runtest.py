#!/usr/bin/python

""" Toplevel script to define the resources available for the test setup
and to run the test cases"""

###########################
## Configuration section ##
###########################

# load zfs test harness configuration settings

ZFS_TH_CONFIG_FILE = 'ZFS.TH.CONFIG'
ZFS_TH_CONFIG      = {"DEVICELIST":"",
                      "BUILDROOT":""
                     }
# read Configuration file to get config data     
try :
    fd = open(ZFS_TH_CONFIG_FILE)
    data = fd.read()
    fd.close()
    sdata = data.split('\n')
    for i in sdata:
        ZFS_TH_CONFIG[i.split('=')[0]] = i.split('=')[1]
except :
    print 

ZFS_TH_CONFIG['DEVICELIST'] = ZFS_TH_CONFIG['DEVICELIST'].split()

# done config read

 
# All the test setup specific detail are in this section. you will
# need to modify this for your test to work correctly.

DEVICELIST = ZFS_TH_CONFIG['DEVICELIST'] 
BUILDROOT  = ZFS_TH_CONFIG['BUILDROOT'] 


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
