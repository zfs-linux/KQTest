#!/usr/bin/python/

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
import os.path
if sys.hexversion < 34013680:
    print "Please run this with a version of python no older than 2.7.1"
    print "A precompiled binary is located at pkgs/ dir in the suite"
    sys.exit(1)

testdir="test"
testfile="*.py"
htmlreport = None

# Currently the arguments are uncomplicated enough that we don't have
# to use getopts

if len(sys.argv) not in [1, 2, 3, 4]:
    usage()
if len(sys.argv) in [3,4] :
    if sys.argv[1] != "-r":
        usage()
    htmlreport = sys.argv[2]
if len(sys.argv) in [2,4]:
    if os.path.isdir(sys.argv[-1]):
        testdir = sys.argv[-1]
	testfile = "*.py"
    else:
	(testdir, testfile) = os.path.split(sys.argv[-1])

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
import lib.HTMLTestRunner


# set path to build
bu = buildSetup(BUILDROOT, globals())
bu.load()

res = resources(host(map(disk, DEVICELIST)))
loader = unittest.TestLoader()
print "loading scripts from "+ testdir
suite = loader.discover(testdir, "__init__.py")
suite = loader.discover(testdir, testfile)  
testsuite = unittest.TestSuite()
testsuite.addTests(suite)
if htmlreport is None:
    unittest.TextTestRunner(verbosity=2).run(suite)
else:
    fp = file(htmlreport, 'wb')
    runner  = lib.HTMLTestRunner.HTMLTestRunner(
                        stream=fp,
                        title='ZFS Unit Test',
                        description='All tests under '+testdir, 
                        verbosity=2
                        )
    runner.run(testsuite)

bu.unload()

def     usage():
    print """
This is the toplevel script to execute all the ZFS test cases. 

python7.1 runtest.py [-r report.html] [startdir] | [filepath]

$ python7.1 runtest.py

Running it without any arguments will result in each unittest being
executed and the summurized result being output to the stdout.

-r         This will generate a html report of the tests run in the specified
           file. If this option is not specified the progress of the tests will 
           be print on the stdout.

startdir   If you want to run a subset of the tests specify the 
           root of the subtree underwhich all test must be executed

filepath   If you want to run any particular script, need to specify the absolute path
           for that script which you want to execute.        
"""
    os.exit(1)
