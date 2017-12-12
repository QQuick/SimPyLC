import numpy

from SimPyLC import *

# Angles are in degrees, gonio functions are defined accordingly in SimPyLC,
# and will also call evaluate
 
def getRotXMat (angleX):
	c = cos (angleX)
	s = sin (angleX)
	return numpy.array ([
		[1, 0, 0],           
		[0, c, -s],
		[0, s, c]
	])

def getRotYMat (angleY):
	c = cos (angleY)
	s = sin (angleY)
	return numpy.array ([
		[c, 0, s],
		[0, 1, 0],
		[-s, 0, c]
	])

def getRotZMat (angleZ):
	c = cos (angleZ)
	s = sin (angleZ)
	return numpy.array ([
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
        angleY = pi / 2.0
        angleX = atan2 (rotMat [0, 1], rotMat [0, 2])
    elif isClose (rotMat [2, 0], 1):
        angleY = -pi / 2
        angleX = atan2 (-rotMat [0, 1], -rotMat [0, 2])
    else:
        angleY = -asin (rotMat [2, 0])
        cosAngleY = cos (angleY)
        angleX = atan2 (rotMat [2, 1] / cosAngleY, rotMat [2, 2] / cosAngleY)
        angleZ = atan2 (rotMat [1, 0] / cosAngleY, rotMat [0, 0] / cosAngleY)
    return numpy.array ([angleX, angleY, angleZ])
    