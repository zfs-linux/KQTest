""" Toplevel script to define the resources available for the test setup
and to run the test cases"""

import types
import unittest
from lib.KQTest import *

kernel("/")
res = resources(host(map(disk, ["sda","sdb", "sdc"])))
print dir(res.get()[0])
suite = unittest.TestLoader().discover("test", "*.py", "test")
#unittest.TextTestRunner(verbosity=2).run(suite)
print "finished"

