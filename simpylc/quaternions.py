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

import numpy

from math import sqrt

from .engine import *

# All angles are in degrees
# All non-scalar variables are numpy arrays

def normized (anArray):
    return anArray / numpy.linalg.norm (anArray)
    
def quatFromAxAng (axis, angle):
    imag =  axis * sin (angle / 2)
    return numpy.array ((cos (angle / 2), imag [0], imag [1], imag [2]))
    
def axAngFromQuat (q):
    angle = 2 * acos (q [0])
    denom = math.sqrt (1 - q [0] * q [0])
    axis = (q [1:] / denom) if denom else numpy.array ((1, 0, 0))
    return axis, angle
    
def quatMul (q0, q1):
    return numpy.array ((
        q0 [0] * q1 [0] - q0 [1] * q1 [1] - q0 [2] * q1 [2] - q0 [3] * q1 [3],
        q0 [0] * q1 [1] + q0 [1] * q1 [0] + q0 [2] * q1 [3] - q0 [3] * q1 [2],
        q0 [0] * q1 [2] - q0 [1] * q1 [3] + q0 [2] * q1 [0] + q0 [3] * q1 [1],
        q0 [0] * q1 [3] + q0 [1] * q1 [2] - q0 [2] * q1 [1] + q0 [3] * q1 [0]       
    ))
        
def quatInv (q):
    return numpy.array ((q [0], -q [1], -q [2], -q [3]))
    
def quatFromVec (v):
    return numpy.array ((0, v [0], v [1], v [2]))
    
def quatVecRot (q, v):
    return (quatMul (
        quatMul (
            q,
            quatFromVec (v)
        ),
        quatInv (q)
    )) [1:]
    
def rotMatFromQuat (q):
    return numpy.array ((
        (1 - 2 * q [2] * q [2] - 2 * q [3] * q [3], 2 * q [1] * q [2] - 2 * q [3] * q [0],     2 * q [1] * q [3] + 2 * q [2] * q [0]),
        (2 * q [1] * q [2] + 2 * q [3] * q [0],     1 - 2 * q [1] * q [1] - 2 * q [3] * q [3], 2 * q [2] * q [3] - 2 * q [1] * q [0]),
        (2 * q [1] * q [3] - 2 * q [2] * q [0],     2 * q [2] * q [3] + 2 * q [1] * q [0],     1 - 2 * q [1] * q [1] - 2 * q [2] * q [2])
    ))
    
