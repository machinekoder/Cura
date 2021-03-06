#!/usr/bin/env python3

# Copyright (c) 2015 Ultimaker B.V.
# Cura is released under the terms of the AGPLv3 or higher.

import os
import sys

#WORKAROUND: GITHUB-704 GITHUB-708
# It looks like setuptools creates a .pth file in
# the default /usr/lib which causes the default site-packages
# to be inserted into sys.path before PYTHONPATH.
# This can cause issues such as having libsip loaded from
# the system instead of the one provided with Cura, which causes
# incompatibility issues with libArcus
if "PYTHONPATH" in os.environ.keys():                       # If PYTHONPATH is used
    PYTHONPATH = os.environ["PYTHONPATH"].split(os.pathsep) # Get the value, split it..
    PYTHONPATH.reverse()                                    # and reverse it, because we always insert at 1
    for PATH in PYTHONPATH:                                 # Now beginning with the last PATH
        PATH_real = os.path.realpath(PATH)                  # Making the the path "real"
        if PATH_real in sys.path:                           # This should always work, but keep it to be sure..
            sys.path.remove(PATH_real)
        sys.path.insert(1, PATH_real)                       # Insert it at 1 after os.curdir, which is 0.

def exceptHook(hook_type, value, traceback):
    import cura.CrashHandler
    cura.CrashHandler.show(hook_type, value, traceback)

sys.excepthook = exceptHook

# Workaround for a race condition on certain systems where there
# is a race condition between Arcus and PyQt. Importing Arcus
# first seems to prevent Sip from going into a state where it
# tries to create PyQt objects on a non-main thread.
import Arcus #@UnusedImport
from UM.Platform import Platform
import cura.CuraApplication
import cura.Settings.CuraContainerRegistry

if Platform.isWindows() and hasattr(sys, "frozen"):
    dirpath = os.path.expanduser("~/AppData/Local/cura/")
    os.makedirs(dirpath, exist_ok = True)
    sys.stdout = open(os.path.join(dirpath, "stdout.log"), "w")
    sys.stderr = open(os.path.join(dirpath, "stderr.log"), "w")

# Force an instance of CuraContainerRegistry to be created and reused later.
cura.Settings.CuraContainerRegistry.getInstance()

app = cura.CuraApplication.CuraApplication.getInstance()
app.run()
