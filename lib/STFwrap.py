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

""" Wrapper module with helper functions and utilities for easy wrapping
the STF test cases with the python harness.

Eventually everything will be part of the python and this wrapper will go away
but for the interim this is required."""

from lib.KQTest import *
import os

def setupEnv():
    env = dict(os.environ)
    env["STF_SUITE"] = KQTest + "/ZFS-Test_Suite" 
    env["STF_TOOLS"] = KQTest + "/ZFS-Test_Suite/STF/usr/src/tools/stf"
    env["ZFSBUILDPATH"] = BUILDROOT
    path = KQTest + "/ZFS-Test_Suite/tests/functional"
    return (env, path)


def runScript(self, script, retcheck=0):
    (newenv, path) = setupEnv()
    fullpath = path + script
    (ret, stdout, stderr) = cmdQuery([fullpath], env=newenv, cwd=os.path.dirname(fullpath))
    self.assertNotIn("ERROR:", stdout, "got:: " + stdout)
    self.assertNotIn("ERROR:", stderr, "got:: " + stderr)
    self.assertEqual(ret, retcheck, "ret: " + str(ret))
    
    
def runScriptArgs(self, scriptlist, retcheck=0):
    (newenv, path) = setupEnv()
    cmd = path + scriptlist[0]
    scriptlist[0] = cmd
    (ret, stdout, stderr) = cmdQuery(scriptlist, env=newenv, cwd=os.path.dirname(scriptlist[0]))
    self.assertNotIn("ERROR:", stdout, "got:: " + stdout)
    self.assertNotIn("ERROR:", stderr, "got:: " + stderr)
    self.assertEqual(ret, retcheck, "ret: " + str(ret))
    
    
