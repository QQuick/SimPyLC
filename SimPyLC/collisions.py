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

from vectors import *

class Box:
    def computeCollisionFields (self):
        self.positionVec = mMul ((0, 0, 0, 1), self.modelViewMatrix)    # OpenGL uses row vectors
        self.radiusVecs = msMul (self.modelViewMatrix [:3], 0.5)        # Radii of inner ellipsoid

def _separate (distanceVec, separAxisVec, boxes):
    projectedDistance = abs (vIpr (distanceVec, separAxisVec))          # Factor |separAxisVec| cancels out below

    print ()
    print (111, distanceVec, separAxisVec, abs (vIpr (distanceVec, separAxisVec)))

    for radiusVec0 in boxes [0] .radiusVecs:
        for radiusVec1 in boxes [1] .radiusVecs:
            print (222, radiusVec0, separAxisVec, abs (vIpr (radiusVec0, separAxisVec)))
            print (333, radiusVec1, separAxisVec, abs (vIpr (radiusVec1, separAxisVec)))
            print (444, abs (vIpr (radiusVec0, separAxisVec)) + abs (vIpr (radiusVec1, separAxisVec)), projectedDistance)
            print (555, abs (vIpr (radiusVec0, separAxisVec)) + abs (vIpr (radiusVec1, separAxisVec)) > projectedDistance)
            if abs (vIpr (radiusVec0, separAxisVec)) + abs (vIpr (radiusVec1, separAxisVec)) > projectedDistance:
                print ('     return not sep   \n')
                return False
        print ()
    else:
        print ('   return separate \n')
        return True

def collision (*boxes):
    distanceVec = vSub (boxes [1] .positionVec, boxes [0] .positionVec)

    for box in boxes:
        for radiusVec in box.radiusVecs:
            if _separate (distanceVec, radiusVec, boxes):
                return False
    '''
    for radiusVec0 in boxes [0] .radiusVecs:
        for radiusVec1 in boxes [1] .radiusVecs:
            if _separate (distanceVec, vOpr (radiusVec0, radiusVec1), boxes):
                print (222, radiusVec0, radiusVec1)
                return False
    '''
    
    print (
        distanceVec,
        boxes [0] .positionVec, '   ',
        boxes [0].radiusVecs, '  -  ',
        boxes [1] .positionVec, '   ',
        boxes [1] .radiusVecs
    )
    
    return True
    
