# -*- coding: utf-8 -*-
"""
pybox_start.py
only a banner and some functions to check the keras version
intentionally lightweight script to speed up the start of PyBox
---------
@author: maikherbig
"""

import os,shutil,json,sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
from pyqtgraph import Qt
import pybox_start #import the module itself only to find out the directory
dir_root = os.path.dirname(pybox_start.__file__)#ask the module for its origin

def splashscreen(icon_suff):
    """
    Use this function to define a splashscreen

    Parameters
    ----------
    icon_suff: str Either ".ico" for Windows/Linux, or ".icns" for MacOS
    
    Returns
    ----------
    QtWidgets.QSplashScreen
    """

    # Create and display the splash screen
    splash_pix = os.path.join(dir_root,"art","icon_splash"+icon_suff)
    splash_pix = QtGui.QPixmap(splash_pix)
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    return splash

def banner():
    #generated using: https://www.patorjk.com/software/taag/
    text = """
  _____       ____             
 |  __ \     |  _ \            
 | |__) |   _| |_) | _____  __ 
 |  ___/ | | |  _ < / _ \ \/ / 
 | |   | |_| | |_) | (_) >  <  
 |_|    \__, |____/ \___/_/\_\ 
         __/ |                 
        |___/                          
is starting...
"""
    print(text)    
    

def keras_json_replace(keras_json_path,json_exists=True):
    if json_exists:
        #Inform user!
        print("I found a keras.json file in your home-directory which has options AID does not accept.\
              This file will be copied to keras_beforeAID_x.json and a new keras.json\
              is written with valid options for AID.")
        i=0
        while os.path.isfile(os.path.expanduser('~')+os.sep+'.keras'+os.sep+'keras_beforeAID_'+str(i)+'.json'):
            i+=1
        shutil.copy(keras_json_path, os.path.expanduser('~')+os.sep+'.keras'+os.sep+'keras_beforeAID_'+str(i)+'.json')
    
    #Write new keras.json:
    with open(os.path.expanduser('~')+os.sep+'.keras'+os.sep+'keras.json','w') as f:
        new_settings = """{\n    "image_dim_ordering": "tf", \n    "epsilon": 1e-07, \n    "floatx": "float32", \n    "backend": "tensorflow"\n}"""                       
        f.write(new_settings)

def keras_json_check(keras_json_path):
    if os.path.isfile(keras_json_path):
        with open(keras_json_path, 'r') as keras_json:
            keras_json=keras_json.read()
        keras_json = json.loads(keras_json)
        keys_keras_json = keras_json.keys() #contained keys 
        keys_expected = ['image_dim_ordering','backend','epsilon','floatx'] #expected keys
        #are those keys present in keys_keras_json?
        keys_present = [key in keys_expected for key in keys_keras_json]
        keys_present = all(keys_present) #are all true?
        checks = []
        if keys_present==True:#all keys are there, now check if the value is correct
            checks.append( keras_json['image_dim_ordering']=="tf" )   
            checks.append( keras_json['backend']=="tensorflow" )    
            checks.append( keras_json['epsilon']==1e-07 )   
            checks.append( keras_json['floatx']=="float32" )    
            checks = all(checks) #are all true?
            if checks==True:
                #keras.json is fine, no need to overwrite it
                return
            else:#some values are different. AID need to write new keras.json
                keras_json_replace(keras_json_path)
        
        else:#some keys are missing
            keras_json_replace(keras_json_path)
    
    else:#there exists NO keras.json! Very likely the user opened AID for the first time :)
        #Welcome the user
        print("A warm welcome to your first session of PyBox :)")
        keras_json_replace(keras_json_path,False)

def pybox_start():
    banner() #show a fancy banner in console

    #BEFORE importing tensorflow or anything from keras: make sure the keras.json has
    #certain properties
    keras_json_path = os.path.expanduser('~')+os.sep+'.keras'+os.sep+'keras.json'
    if not os.path.isdir(os.path.expanduser('~')+os.sep+'.keras'):
        os.mkdir(os.path.expanduser('~')+os.sep+'.keras')
    
    keras_json_check(keras_json_path)#check the keras.json
    
    from tensorflow.python.client import device_lib
    devices = device_lib.list_local_devices()
    device_types = [devices[i].device_type for i in range(len(devices))]
    
    #Get the number  of CPU cores and GPUs
    cpu_nr = os.cpu_count()
    gpu_nr = device_types.count("GPU")
    print("Nr. of GPUs detected: "+str(gpu_nr))
    
    print("Found "+str(len(devices))+" device(s):")
    print("------------------------")
    for i in range(len(devices)):
        print("Device "+str(i)+": "+devices[i].name)
        print("Device type: "+devices[i].device_type)
        print("Device description: "+devices[i].physical_device_desc)
        print("------------------------")
    
    #Split CPU and GPU into two lists of devices
    devices_cpu = []
    devices_gpu = []
    for dev in devices:
        if dev.device_type=="CPU":
            devices_cpu.append(dev)
        elif dev.device_type=="GPU":
            devices_gpu.append(dev)
        else:
            print("Unknown device type:"+str(dev)+"\n")
    
    from keras import backend as K
    if 'GPU' in device_types:
        keras_gpu_avail = K.tensorflow_backend._get_available_gpus()
        if len(keras_gpu_avail)>0:
            print("Following GPU is used:")
            print(keras_gpu_avail)
            print("------------------------")
        else:
            print("TensorFlow detected GPU, but Keras didn't")
            print("------------------------")


def pybox_main(icon_suff):
    """
    Function defines the main loop (starts GUI)

    Parameters
    ----------
    icon_suff: str Either ".ico" for Windows/Linux, or ".icns" for MacOS
    
    Returns
    ----------
    QtWidgets.QApplication
    QtWidgets.QMainWindow
    """

    import frontend #frontend.py contains most of the "intelligence" 
    global app
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(dir_root,"art","icon_main"+icon_suff)))
    MainWindow = QtWidgets.QMainWindow()
    ui = frontend.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    return app,MainWindow

    