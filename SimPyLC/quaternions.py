import numpy

from .engine import *

# All angles are in degrees
# All multidimensional variables are numpy arrays

def normize (anArray):
    anArray /= numpy.linalg.norm (anArray)
    
def quatFromAxAng (axis, angle):
    imag = axis * sin (angle / 2)
    return numpy.array ((cos (angle / 2), imag [0], imag [1], imag [2]))
    
def axAngFromQuat (q):
    imag = q [1:]
    imagLen = numpy.linalg.norm (imag)
    return imag / imagLen if imagLen else numpy.array ((1, 0, 0)), 2 * atan2 (imagLen, q [0])
    
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
    ) / 2) [1:]
    
def rotMatFromQuat (q):
    return numpy.array ((
        (1 - 2 * q [2] * q [2] - 2 * q [3] * q [3], 2 * q [1] * q [2] - 2 * q [3] * q [0],     2 * q [1] * q [3] + 2 * q [2] * q [0]),
        (2 * q [1] * q [2] + 2 * q [3] * q [0],     1 - 2 * q [1] * q [1] - 2 * q [3] * q [3], 2 * q [2] * q [3] - 2 * q [1] * q [0]),
        (2 * q [1] * q [3] - 2 * q [2] * q [0],     2 * q [2] * q [3] + 2 * q [1] * q [0],     1 - 2 * q [1] * q [1] - 2 * q [2] * q [2])
    ))
    