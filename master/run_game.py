#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import os

#try:
    #libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    #sys.path.insert(0, libdir)
    #import main
#except:
    ## probably running inside py2exe which doesn't set __file__
    #from lib import main
    #pass

def change_to_correct_path():
    exe_base_dir = sys.argv[0]
    real_curdir = os.path.realpath(os.curdir)
    base_dir = os.path.split(exe_base_dir)[0]
    exe_base_dir = os.path.join(real_curdir, base_dir)
    os.chdir(exe_base_dir)
    sys.path.append(exe_base_dir)
    real_curdir = os.path.realpath(os.curdir)

change_to_correct_path()

from lib import main

if '-profile' in sys.argv:
    import profile
    profile.run('main.main()')
else:
    main.main()
