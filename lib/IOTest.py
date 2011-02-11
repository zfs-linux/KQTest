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

"""Library to generate various kinds of IO loads
"""

import subprocess
import unittest
import threading
import os
from lib.KQTest import *

NOTSTARTED = 0
RUNNING = 1
DONE = 2
VERIFYING = 3
ALLDONE = 4

iotestexec = KQTest+"/iotest/iotest"

class fsop():
    """This is the base class which defines all operations performable 
    at the file i/o interface level"""

    def __init__(self):
        self.idle = True
        self.state = NOTSTARTED

    def run(self):
        """
        run the iotest operation
        Something is wrong with your test case if this gets called"""
        raise Exception("abstact class called unexpectedly")

    def verify(self):
        """Verify the iotest operation perviously run
        Something is wrong with your test case if this gets called"""
        raise Exception("abstact class called unexpectedly")

    def delete(self):
        """Remove the file that had been created
        Something is wrong with your test case if this gets called"""
        raise Exception("abstact class called unexpectedly")



class iotest(fsop):
    """Class which executes the iotest utility"""

    def __init__(self, outfile, fs, woff=0, wcount=1, wiosize=4096, thrds=1, seq=True, sparse=False, sparseFactor=None,method="bufferedio", verbose=False):
        """    method can be one of bufferedio,directio or mmap"""
        fsop.__init__(self)
        self.outfile = outfile
        self.woff = woff
        self.wcount = wcount
        self.wiosize = wiosize
        self.thrds = thrds
        self.seq = seq
        self.sparse = sparse
        if sparseFactor != None:
            self.sparseFactor = sparseFactor
        self.method = method
        self.verbose = verbose
        self.pattern = ""
        self.ret = ""
        assert(self.state == NOTSTARTED)

    def run(self):

        run=[]
        run.append(iotestexec)
        run.append("-o") 
        run.append(self.outfile)
        run.append("-w")
        run.append("offset="+str(self.woff)+",count="+str(self.wcount)+",iosize="+str(self.wiosize))
        run.append("-y")
        run.append(str(self.thrds))
        run.append("-q")
        if(self.seq):
            run.append("seq")
        else:
            run.append("random")
        run.append("-t")
        if(self.sparse):
            run.append("sparse")
        else:
            run.append("non-sparse")
        run.append("-k")
        run.append(self.method)
        if hasattr(self, "sparseFactor"):
            run.append("-s")
            run.append(self.sparseFactor)
        print run
        self.pattern = " ".join(run)
        run.append("-P")
        run.append(self.pattern)
        print "write cmd:" + " ".join(run)
        (self.ret, dummy, dummy) = cmdQuery(run)
        self.state = RUNNING
    
    def verify(self, method="bufferedio"):
        """ method can be one of bufferedio,directio or mmap"""
        self.proc=VERIFYING
        run=[]
        run.append(iotestexec)
        run.append("-V")
        run.append("-i") 
        run.append(self.outfile)
        run.append("-r")
        run.append("offset="+str(self.woff)+",count="+str(self.wcount)+",iosize="+str(self.wiosize))
        run.append("-x")
        run.append(str(self.thrds))
        run.append("-q")
        if(self.seq):
            run.append("seq")
        else:
            run.append("random")
        run.append("-t")
        if(self.sparse):
            run.append("sparse")
        else:
            run.append("non-sparse")
        run.append("-f")
        run.append(self.method)
        if hasattr(self, "sparseFactor"):
            run.append("-s")
            run.append(self.sparseFactor)
        run.append("-P")
        run.append(self.pattern)
        (ret, dummy, dummy) = cmdQuery(run)
        if ret != 0:
            raise Exception("verify failed")

class nameGen():
    """simple file name generator fuction."""

    def __init__(self, fs, newdir):
        self.fs = fs
        os.mkdir(fs.mntpt +newdir)
        self.basename= fs.mntpt +newdir+"/"
        self.counter = 0

    def getGen(self):
        while True:
            self.counter += 1
            yield self.basename+str(self.counter)
            
        
class loadGen():
    """Generator funtion which generates the work load  iotest objects that 
    can be run by the individual threads """

    def __init__(self, fs, namegen, seq = [True, False], sparseFactor = [ None, 1, None, 2, 7, None, 13, 15],
                 thrds = [1, 1, 2, 3, 5, 5, 11], wcount = [456, 567, 8, 256, 10013, 512, 1024, 4096], 
                 wiosize = [200, 512, 900, 1024, 2048, 5000, 8192, 12000], 
                 woff = [512, 1536, 4096, 0, 8192, 16384, 20480], 
                 method = ["mmap", "bufferedio", "directio"], sparse = [False, True],
                 verifymethod = ["mmap", "bufferedio", "directio"]):
        self.fs = fs
        self.nameget = namegen
        self.seq = seq
        self.sparseFactor = sparseFactor
        self.thrds = thrds
        self.wcount = wcount
        self.wiosize = wiosize
        self.woff = woff
        self.method = method
        self.sparse = sparse
        self.verifymethod = verifymethod
        # the order in which we iterate over the parameters
        self.order = ["seq", "sparseFactor", "thrds", "wcount", "wiosize", "woff", "method"]
        self.current = 0
        self.total = 1
        # the product of all the list is the number of iotimes we will have
        for i in self.order:
            self.total *= len(getattr(self, i))
            
    def runtests(self, (curr, total, test)):
        print "running "+str(curr)+" of "+str(total)
        test.run()
        test.verify()
        

    def getIOTest(self, param = 0, paramdict={}):
        if param == len(self.order):
            self.current += 1
            yield (self.current, self.total, iotest(self.nameget.next(), self.fs, **paramdict))
            return
        for i in getattr(self, self.order[param]):
            paramdict[self.order[param]] = i 
            for j in  self.getIOTest(param + 1, dict(paramdict)):
                yield j
            
