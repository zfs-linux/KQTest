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
_CLEANUP = ""
# Perform cleanup and exit 
#
# code - stf exit code
# msg - message text

def _endlog(code,msg):    
    logfile="/tmp/log.$$"
    global _CLEANUP
    #_recursive_output $logfile
    if _CLEANUP != "":
        cleanup=_CLEANUP
        log_onexit("")
        log_note("Performing local cleanup via log_onexit")
	cleanup()
    exitcode=code
    if msg != "":
        _printline(msg)
    exit(exitcode)



# Set an exit handler
#
#  - function(s) to perform on exit
#
# Exit functions
#

# Perform cleanup and exit STF_PASS
#
# msg - message text

def log_pass(msg):
    _endlog(STF_PASS,msg)

# Perform cleanup and exit STF_FAIL
#
# msg - message text

def log_fail(msg):
    _endlog(STF_FAIL,msg)

# Perform cleanup and exit STF_UNRESOLVED
#
# msg - message text

def log_unresolved(msg):
    _endlog(STF_UNRESOLVED,msg)

# Perform cleanup and exit STF_NOTINUSE
#
# msg - message text

def log_notinuse(msg):
    _endlog(STF_NOTINUSE,msg)

# Perform cleanup and exit STF_UNSUPPORTED
#
# msg - message text

def log_unsupported(msg):
    _endlog(STF_UNSUPPORTED,msg)

# Perform cleanup and exit STF_UNTESTED
#
# msg - message text

def log_untested(msg):
    _endlog(STF_UNTESTED,msg)

# Perform cleanup and exit STF_UNINITIATED
#
# msg - message text


def log_uninitiated(msg):
    _endlog(STF_UNINITIATED,msg)


# Perform cleanup and exit STF_NORESULT
#
# msg - message text

def log_noresult(msg):
    _endlog(STF_NORESULT,msg)

# Perform cleanup and exit STF_WARNING
#
# msg - message text

def log_warning(msg):
    _endlog(STF_WARNING,msg)

# Perform cleanup and exit $STF_TIMED_OUT
#
# msg - message text

def log_timed_out(msg):
    _endlog(STF_TIMED_OUT,msg)

# Perform cleanup and exit $STF_OTHER
#
# msg - message text

def log_other(msg):
    _endlog(STF_OTHER,msg)

def log_onexit(func):
    global _CLEANUP
    _CLEANUP = _CLEANUP + func
    print "func " +_CLEANUP

def log_pos(command):
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    count = 1
    while ( count < length):
         process2 = subprocess.Popen(command[count],stdin=process1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
         process1 = process2
         count = count + 1
    data, err = process1.communicate()
    statuscode =  process1.wait()
    return (data, statuscode)

def cmdExecute_on_stderr(command):
    length = len(command)
    if length == 0:
        return 0
    process1 = subprocess.Popen(command[0],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
    global _CLEANUP
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



