from numpy import *
from transform import *

angleX = 0
angleY = -130
angleZ = 0

print (angleX, angleY, angleZ)

for i in range (10000):
    rotMat = getRotZMat (angleZ) @ getRotYMat (angleY) @ getRotXMat (angleX)
    angleX, angleY, angleZ = (getXyzAngles (rotMat))
    
print (angleX, angleY, angleZ)
