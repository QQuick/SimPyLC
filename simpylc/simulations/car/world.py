'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import os
import sys as ss
import time as tm

ss.path +=  [os.path.abspath (relPath) for relPath in  ('../../..', '..')]   # If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable
scannerType = 'lidar' if input ('Lidar or sonar <l/s>: ') == 'l' else 'sonar'  # Should be done prior to any SimPyLC related imports due to concurrency

import simpylc as sp

import control_server as cs
import physics as ps
import visualisation as vs

vs.scannerType = scannerType

sp.World (
    cs.ControlServer,
    ps.Physics,
    vs.Visualisation
)
