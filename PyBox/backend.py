# -*- coding: utf-8 -*-
"""
backend
---------
@author: maikherbig
"""
import os,shutil,json
import io,sys
import frontend
dir_root = os.path.dirname(frontend.__file__)#ask the module for its origin


def run_python(code):
    codeOut = io.StringIO()
    out,error = "",""
    # capture output
    sys.stdout = codeOut
    try:
        exec(code,globals())
    except Exception as e:
        error = str(e)
    # restore stdout
    sys.stdout = sys.__stdout__
    out = codeOut.getvalue()
    codeOut.close()
    
    return out,error




