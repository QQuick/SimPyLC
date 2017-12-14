from numpy import *

from .engine import *

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
    
def vDiv (v, x):
    return (v [0] / x [0], v [1] / x [1], v [2] / x [2])

def vsDiv (v, x):
    return (v [0] / x, v [1] / x, v [2] / x)
   
def vNor (v):
    return sqrt (v [0] * v [0] + v [1] * v[1] + v [2] * v [2])
    
def vUni (v):
    return divide (v, tNor (v))
    
# 3D matrices
    
def mInv (m):
    return numpy.invert (numpy.array (m)) .tolist ()
    
# Quaternions (angles in degrees)

def qJoi (axis, angle):
    s = sin (angle)
    return (cos (angle), s * axis [0], s * axis [1], s * axis [2])
    
def qSpli (q):
    angle = acos (q [0)]
    s = sin (angle)
    axis = (q [1] / s, q [2] / s, q [3] / s)
    
def qMul (q0, q1):
    return  (
        +q0 [0] * q1 [0] - q0 [1] * q1 [1] - q0 [2] * q1 [2] - q0 [3] * q1 [3],
        +q0 [0] * q1 [1] + q0 [1] * q1 [0] + q0 [2] * q1 [3] - q0 [3] * q1 [2],
        +q0 [0] * q1 [2] - q0 [1] * q1 [3] + q0 [2] * q1 [0] + q0 [3] * q1 [1],
        +q0 [0] * q1 [3] + q0 [1] * q1 [2] - q0 [2] * q1 [1] + q0 [3] * q1 [0]       
    )
    
def qsMul (q, s):
    return (q [0] * s, q [1] * s, q [2] * s, q [3] * s)
    
def qsDiv (q, s):
    return (q [0] / s, q [1] / s, q [2] / s, q [3] / s)
    
def qInv (q):
    return (q [0], -q [1], -q [2]. -q [3])
    
def qvRot (q, v):
    return qsDiv (
        qMul (
            qMul (
                q,
                (0, v [0], v [1], v [2])
            ),
            qInv (q))
        ),
        2
    ) [1 : ]
    
def qmRot (q, m):
    m = numpy.array (m)
    m [ : , 0] = qvRot (m [ : , 0]
    m [ : , 0] = qvRot (m [ : , 1]
    m [ : , 0] = qvRot (m [ : , 2]
    return m
    