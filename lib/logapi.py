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

# This is a ksh function library. It is intended to be sourced into
# other ksh scripts and not executed directly.

from KQTest import *
import os
import subprocess
import sys

STF_PASS=0
STF_FAIL=1
SUCCESS = 0
FAIL = 1
STF_UNSUPPORTED=4
STF_UNRESOLVED=5

def log_pos(command):
    print "args to logmust :",
    print command
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    print process1.stdout 
    count = 1
    while ( count < length):
         process2 = subprocess.Popen(command[count],stdin=process1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
         process1 = process2
         count = count + 1
    data, err = process1.communicate()
    statuscode =  process1.wait()
    print "STATUS CODE : ",statuscode
    if statuscode != SUCCESS:
      _printerror(command)
    else:
      _printsuccess(command)
    return (statuscode)


def log_notpos(command):
    print "args to log_mustnot :",
    print command
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    print process1.stdout 
    count = 1
    while ( count < length):
         process2 = subprocess.Popen(command[count],stdin=process1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
         process1 = process2
         count = count + 1
    data, err = process1.communicate()
    statuscode =  process1.wait()
    print "STATUS CODE : ",statuscode
    if statuscode != SUCCESS:
        _printsuccess(command)
    else:
        _printerror(command)
    return (statuscode)


def cmdExecute(command):
    print "args to cmdExecute :",
    print command
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    print process1.stdout 
    count = 1
    while ( count < length):
         process2 = subprocess.Popen(command[count],stdin=process1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
         process1 = process2
         count = count + 1
    data, err = process1.communicate()
    statuscode =  process1.wait()
    return (data, statuscode)

def cmdExecute_on_stderr(command):
    print "args to cmdExecute_on_stderr :",
    print command
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    print process1.stdout 
    count = 1
    while ( count < length):
         process2 = subprocess.Popen(command[count],stdin=process1.stderr,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
         process1 = process2
         count = count + 1
    data, err = process1.communicate()
    statuscode =  process1.wait()
    return (data, statuscode)

    
def log_must(command):
    ret = log_pos(command)
    if ret != SUCCESS:
       log_fail("")

    
def log_mustnot(command):
    ret = log_notpos(command)
    if ret == SUCCESS:
       log_fail("")

def log_onexit(func):
    _CLEANUP = func

def log_assert(command):
    _printline("ASSERTION :"+command)    

def log_note(command):
    _printline("NOTE :"+command)

def _printline(command):
    print command

def _printerror(command):
    print "ERROR: ",command

def _printsuccess(command):
    print "SUCCESS: ",command

def log_fail(str):
    _endlog(STF_FAIL,str)


def _endlog(STF_val,str):
    print str
    sys.exit(STF_val)

def log_pass(str):
    _endlog(STF_PASS,str)

def log_unsupported(str):
    _endlog(STF_UNSUPPORTED,str)

def log_unresolved(str):
   _endlog(STF_UNRESOLVED,str)
