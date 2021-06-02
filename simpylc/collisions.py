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

'''
A beam can have a collision id.
Beams with the same collision id are accumulated in a group.
Each group obtains a bounding sphere to avoid some needless work.

As soon as the bounding spheres of two groups overlap,
the OBB SAT method is applied to all their beams.

Separation axes are
    3 edges for A
    3 edges for B
    3 x 3 cross products between those edges
'''

from .vectors import *

class Box:
    def __init__ (self):
        # OpenGL uses row vectors
        
        self.startPositionVec = (0, 0, 0, 1)

        self.startBaseVecs = msMul ((
            (0, 0, 1),
            (0, 1, 0),
            (1, 0, 0)
        ), 0.5) [:3]


        self.startEdgeVecs = msMul ((
            ( 1,  1,  1),
            ( 1,  1, -1),
            ( 1, -1,  1),
            (-1,  1,  1)
        ), 0.5)

    def computeCollisionFields (self):
        self.positionVec = mMul (self.startPositionVec, self.modelViewMatrix)
        
        rotationMatrix = self.modelViewMatrix [:3]                              # Leave out translation row (OpenGL uses row vectors
        self.baseVecs = mMul (self.startBaseVecs, rotationMatrix)
        self.edgeVecs = mMul (self.startEdgeVecs, rotationMatrix)

def _separate (distanceVec, separAxisVec, boxPair):
    projectedDistance = abs (vIpr (distanceVec, separAxisVec))                  # Factor |separAxisVec| cancels out below
    
    for edgeVec0 in boxPair [0] .edgeVecs:
        for edgeVec1 in boxPair [1] .edgeVecs:
        
            # Test for >= rather than >, since if baseVecs are parallel, separAxisVec will be 0 vec, so inner prods all 0

            if abs (vIpr (edgeVec0, separAxisVec)) + abs (vIpr (edgeVec1, separAxisVec)) >= projectedDistance:
                return False
    else:
        return True

def collision (*boxPair):
    distanceVec = vSub (boxPair [1] .positionVec, boxPair [0] .positionVec)

    # Try 2 x 3 base vectors as possible separation axes
    
    for box in boxPair:
        for baseVec in box.baseVecs:
            if _separate (distanceVec, baseVec, boxPair):
                return False
    
    # Try 3 x 3 outer products of base vectors as possible separation axes
    
    for baseVec0 in boxPair [0] .baseVecs:
        for baseVec1 in boxPair [1] .baseVecs:
            if _separate (distanceVec, vOpr (baseVec0, baseVec1), boxPair):
                return False
    
    # None of the possible separation axes held up, so it's a collision
    return True
    
