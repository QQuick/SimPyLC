import numpy

from SimPyLC import *

# Angles are in degrees, sin and cos are defined accordingly in SimPyLC,
# and will also call evaluate
	
def getRotXMat (angle):
	c = cos (angle)
	s = sin (angle)
	return numpy.matrix ([
		[1, 0, 0, 0],           
		[0, c, -s, 0],
		[0, s, c, 0],
		[0, 0, 0, 1]
	])

def getRotYMat (angle):
	c = cos (angle)
	s = sin (angle)
	return numpy.matrix ([
		[c, 0, s, 0],
		[0, 1, 0, 0],
		[-s, 0, c, 0],
		[0, 0, 0, 1]
	])

def getRotZMat (angle):
	c = cos (angle)
	s = sin (angle)
	return numpy.matrix ([
		[c, -s, 0, 0],
		[s, c, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
    