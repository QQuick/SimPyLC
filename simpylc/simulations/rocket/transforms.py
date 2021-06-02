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

import numpy as np

import simpylc as sp

# Angles are in degrees, gonio functions are defined accordingly in SimPyLC,
# and will also call evaluate
 
def getRotXMat (angleX):
	c = sp.cos (angleX)
	s = sp.sin (angleX)
	return np.array ([
		[1, 0, 0],           
		[0, c, -s],
		[0, s, c]
	])

def getRotYMat (angleY):
	c = sp.cos (angleY)
	s = sp.sin (angleY)
	return np.array ([
		[c, 0, s],
		[0, 1, 0],
		[-s, 0, c]
	])

def getRotZMat (angleZ):
	c = sp.cos (angleZ)
	s = sp.sin (angleZ)
	return np.array ([
		[c, -s, 0],
		[s, c, 0],
		[0, 0, 1]
	])
    
def isClose(x, y):
    return abs (x - y) <= 1e-8 + 1e-5 * abs (y)

def getXyzAngles (rotMat):  # rotMat == rotMatZ @ rotMatY @ rotMatX
    # Source: Computing Euler angles from a rotation matrix, by Gregory G. Slabaugh
    # http://thomasbeatty.com/MATH%20PAGES/ARCHIVES%20-%20NOTES/Applied%20Math/euler%20angles.pdf
    angleZ = 0
    if isClose (rotMat [2, 0], -1):
        angleY = sp.pi / 2.0
        angleX = sp.atan2 (rotMat [0, 1], rotMat [0, 2])
    elif isClose (rotMat [2, 0], 1):
        angleY = -sp.pi / 2
        angleX = sp.atan2 (-rotMat [0, 1], -rotMat [0, 2])
    else:
        angleY = -sp.asin (rotMat [2, 0])
        cosAngleY = sp.cos (angleY)
        angleX = sp.atan2 (rotMat [2, 1] / cosAngleY, rotMat [2, 2] / cosAngleY)
        angleZ = sp.atan2 (rotMat [1, 0] / cosAngleY, rotMat [0, 0] / cosAngleY)
    return np.array ([angleX, angleY, angleZ])
    
def modifiedGramSchmidt (rotMat): # Numpy QR factorization can't be used, since it gives a Q with a changed orientation
    
    # Create references to column vectors
    t = rotMat [ : , 0]
    n = rotMat [ : , 1]
    b = rotMat [ : , 2]
    
    # Normalize T
    t /= np.linalg.norm (t)
    
    # Remove projection of T from N and normalize
    n -= t * np.dot (n, t)
    n /= np.linalg.norm (n)
    
    # Compute B perpendicular to T and N with right orientation
    # Remove projection of 
    b -= t * np.dot (b, t)
    b -= n * np.dot (b, n)
    b /= np.linalg.norm (b)
