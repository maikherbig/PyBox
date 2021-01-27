# -*- coding: utf-8 -*-
"""
pybox_start.py
only a banner and some functions to check the keras version
intentionally lightweight script to speed up the start of PyBox
---------
@author: maikherbig
"""

import numpy as np
import matplotlib.pyplot as plt

def pybox_start():
    a = np.linspace(start=-10.0,stop=10,num=1000)
    b = a**2
   
    plt.figure(1,figsize=(4,4))
    plt.scatter(a,b,s=10,c="cornflowerblue",linewidth="0",facecolors='none',edgecolors='black',alpha=1)
    plt.xlabel("x")
    plt.ylabel("y")
    
    plt.grid()
    plt.xlim(-10,10)
    plt.show()


    