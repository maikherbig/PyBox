# -*- coding: utf-8 -*-
"""
pybox: This is a software bundle containing Python and lots of Python packages preinstalled
#######################Run this script to start the app########################
-> Serve your app to any PC or Mac.
---------
@author: maikherbig
"""
__version__ = "0.1.0" #version number of pybox

import os,sys,gc

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
from pyqtgraph import Qt
import pybox_start

print("PyBox version: "+__version__)

#suppress warnings/info from tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#determine the Operating system
if not sys.platform.startswith("win"):
    from multiprocessing import freeze_support
    freeze_support()
# Make sure to get the right icon file on win,linux and mac
if sys.platform=="darwin":
    icon_suff = ".icns"
else:
    icon_suff = ".ico"

##########################Optional: Splash-screen #############################
##################(Only use it if you also have a frontend)####################
try:
    splashapp = QtWidgets.QApplication(sys.argv)
    # Create and display the splash screen
    splash = pybox_start.splashscreen(icon_suff)
except:
    pass

########################Required: some script to execute#######################
pybox_start.pybox_start()#Could be a banner. Or, you could put your whole script into pybox_start and only exectute this

##############################Optional: GUI####################################
#import frontend #import frontend very late such that the splashscreen loads fast

dir_root = os.path.dirname(pybox_start.__file__)#ask the module for its origin
def main():
    app,MainWindow = pybox_start.pybox_main(icon_suff)
    
    try:
        splash.finish(MainWindow)
    except:
        pass

    ret = app.exec_()
    sys.exit(ret)

if __name__ == '__main__':
    try:
        main()
    except:
        pass






