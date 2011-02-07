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
    
    
