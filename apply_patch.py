#!/usr/bin/env python

################################################################################
# NAME: Script for applying patch
# VERSION: 0.0.1
# AUTHOR: Vu Thanh Cong
# DATE: 14/Dec/2016
################################################################################
# How to use!
# 1. Create folder [patches] under ANDROID_ROOT
# 2. Copy this script apply_patch.py to folder [patches]
# 3. Copy all patches folder to folder [patches]
# 4. Run ./apply_patch.sh
################################################################################

import sys
import os
from subprocess import Popen, PIPE, STDOUT

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(argv):
    # Check current directory
    cwd = os.getcwd()
    android_root = os.path.abspath(os.path.join(cwd, os.pardir))
    #if not os.path.exists(android_root + "/.repo"):
    #    print bcolors.WARNING + "This folder is not under root of Android source tree!" + bcolors.ENDC
    #    sys.exit(1)
    # Iterate all directory and apply patch
    dirs = os.walk(cwd).next()[1]
    success=0
    fail=0
    for folder in dirs:
        project_dir = android_root + "/" + folder.replace("-","/")
        patch_dir = cwd + "/" + folder
        if not os.path.exists(project_dir):
            print (bcolors.WARNING + "[{}] not exists" + bcolors.ENDC).format(project_dir)
            os.makedirs(project_dir)
            git_init(project_dir)

        ret = git_am(project_dir, patch_dir)
        if ret == 0:
            success += 1
        else:
            fail += 1
    print (bcolors.OKGREEN + "Success: {0}" + bcolors.FAIL + " / Failed: {1}" + bcolors.ENDC).format(success, fail)
    print "!DONE!"

def git_init(project_dir):
    MOVE_TO_DIR = "cd {}".format(project_dir)
    INIT_CMD = "git init"
    FULL_CMD = "{0} && {1}".format(MOVE_TO_DIR, INIT_CMD)
    process = Popen(FULL_CMD, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    t = process.communicate()[0]
    rc = process.returncode
    if rc!=0:
        print t
    return rc

def git_am(project_dir, patch_dir):
    MOVE_TO_DIR = "cd {}".format(project_dir)
    AM_CMD = "git am --quiet {}/*.patch".format(patch_dir)
    FULL_CMD = "{0} && {1}".format(MOVE_TO_DIR, AM_CMD)
    process = Popen(FULL_CMD, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    t = process.communicate()[0]
    rc = process.returncode
    retmsg = (bcolors.OKGREEN + "[OK]" + bcolors.ENDC) if rc==0 else (bcolors.FAIL + "[Failed]" + bcolors.ENDC)
    project_dir_colored = (bcolors.OKBLUE + "[{}]" + bcolors.ENDC).format(project_dir)
    print "=> Applying to {0} ...... {1}".format(project_dir_colored, retmsg)
    if rc!=0:
        print t
    return rc


if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print
    except EOFError:
        print
