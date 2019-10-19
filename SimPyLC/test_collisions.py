import collisions as cl

class Box:
    pass
    
box0 = Box ()
box0.positionVec = (0, 0, 0)
box0.radiusVecs =  ((1, 0, 0), (0, 1, 0), (0, 0, 1))


box1 = Box ()
box1.positionVec = (-1.3, 1.3, 0)
box1.radiusVecs = ((0.707, -0.707, 0), (0.707, 0.707, 0), (0, 0, 1))

print (cl.collision (box0, box1))
