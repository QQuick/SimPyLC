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

from numpy import *

#from .engine import *

# 3D vectors

def vEva (v):
    return (evaluate (v [0]), evaluate (v [1]), evaluate (v [2]))
                
def vNeg (v):
    return (-v [0], -v [1], -v [2])
    
def vAdd (v0, v1):
    return (v0 [0] + v1 [0], v0 [1] + v1 [1], v0 [2] + v1 [2])
    
def vSub (v0, v1):
    return (v0 [0] - v1 [0], v0 [1] - v1 [1], v0 [2] - v1 [2])
        
def vMul (v0, v1):
    return (x [0] * v [0], x [1] * v [1], x [2] * v [2])
    
def vsMul (v, x):
    return (v [0] * x, v [1] * x, v [2] * x)
    
def vDiv (v0, v1):
    return (v0 [0] / v1 [0], v0 [1] / v1 [1], v0 [2] / v1 [2])

def vsDiv (v, x):
    return (v [0] / x, v [1] / x, v [2] / x)
   
def vNor (v):
    return sqrt (v [0] * v [0] + v [1] * v[1] + v [2] * v [2])
    
def vUni (v):
    return divide (v, tNor (v))
    
def vIpr (v0, v1):
    return v0 [0] * v1 [0] + v0 [1] * v1 [1] + v0 [2] * v1 [2]

def vOpr (v0, v1):
    return (
        v0 [1] * v1 [2] - v0 [2] * v1 [1],
        v0 [2] * v1 [0] - v0 [0] * v1 [2],
        v0 [0] * v1 [1] - v0 [1] * v1 [0]
    )
    
# Square matrices

'''   
def mInv (m):
    return invert (array (m)) .tolist ()
'''

def msMul (m, s):
    return (array (m) * s) .tolist ()

def mMul (m0, m1):
    return matmul (array (m0), array (m1)) .tolist ()
    
def mTra (m):
    return transpose (array (m)) .tolist ()
    
