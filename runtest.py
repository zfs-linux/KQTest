#!/usr/bin/python

# Copyright (c) 2010 Knowledge Quest Infotech Pvt. Ltd. 
# Produced at Knowledge Quest Infotech Pvt. Ltd. 
# Written by: Knowledge Quest Infotech Pvt. Ltd. 
#             zfs@kqinfotech.com
#
# This software is NOT free to use and you cannot redistribute it
# and/or modify it. You should be possesion of this software only with
# the explicit consent of the original copyright holder.
#
# This is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.


""" Toplevel script to define the resources available for the test setup
and to run the test cases"""

### Check version of Python
import sys
if sys.hexversion < 34013680:
    print "Please run this with a version of python no older than 2.7.1"
    print "A precompiled binary is located at pkgs/ dir in the suite"
    sys.exit(1)

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
        if len(i) > 0:
            # check whether line is comment line or not
            if i.count('#') == 0:
                # basic format check for parameter and value
                if (i.count('=') == 1) and (len(i) >2) and (i[0]!='=') : 
                    globals()[i.split('=')[0]] = i.split('=')[1]
                else:
                    print "Wrong configuration : " + i
except :
    print "Error reading config file"



# The device list must be a list not a string of device names
DEVICELIST = DEVICELIST.split()

# Path names which must terminate with a /
for i in ["BUILDROOT", "KQTest"]:
    if len(globals()[i]) != 0 and (globals()[i])[-1] != "/":
             globals()[i] +="/"
    
# done config read
 

###########################
## end of config section ##
###########################

import types
import unittest
from lib.KQTest import *
import sys                              


# set path to build
bu = buildSetup(BUILDROOT, globals())
bu.load()

res = resources(host(map(disk, DEVICELIST)))
loader = unittest.TestLoader()
if len(sys.argv) == 2:
    print "loading scripts from "+ sys.argv[0]
    suite = loader.discover(sys.argv[1], "*.py")
else: 
        suite = loader.discover("test", "*.py")
unittest.TextTestRunner(verbosity=2).run(suite)
print "finished"

bu.unload()
