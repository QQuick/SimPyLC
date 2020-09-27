'''
Inputs:

- A lidar distance array with a resolution of 1 degree
- An x, y position and course angle of the car

Outpus:

- Acceleration stepper output

'''

import time as tm

import simpylc as sp

class LidarPilot:
    noObstacle = (sp.finity, 0)

    def __init__ (self):
        self.lidar = self.world.visualisation.lidar
        
        while True:
            self.readInputs ()
            self.sweep ()
            self.writeOutputs ()
            tm.sleep (0.02)
            
            
    def readInputs (self):
        self.nearestObstacles = [self.noObstacle, self.noObstacle]
        
        for lidarAngle in range (-self.lidar.halfApertureAngle, self.lidar.halfApertureAngle):
            lidarDistance = self.lidar.distances [lidarAngle]
            if lidarDistance < self.nearestObstacles [0][0]:
                self.nearestObstacles [0] = (lidarDistance, lidarAngle)
            elif lidarDistance < self.nearestObstacles [1][0]:
                self.nearestObstacles [1] = (lidarDistance, lidarAngle)
                                                                                                                                
        self.targetObstacle = sp.tsDiv (sp.tAdd (*self.nearestObstacles), 2)
        
        self.velocity = self.world.physics.velocity
        self.steeringAngle = self.world.physics.steeringAngle

    def sweep (self):
        self.steeringAngle = self.targetObstacle [1]

    def writeOutputs (self):
        self.world.physics.steeringAngle.set (self.steeringAngle)
        
