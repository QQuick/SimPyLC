import time as tm
import traceback as tb

import simpylc as sp

class LidarPilot:
    def __init__ (self):
        print ('Press enter to start or stop...')
        
        '''
        self.driveEnabled = False
        
        while True:
            self.input ()
            self.sweep ()
            self.output ()
            tm.sleep (0.02)
        '''
        
    def input (self):
        key = sp.getKey ()
        
        if key == 'KEY_ENTER':
            self.driveEnabled = not self.driveEnabled
        
        self.nearestObstacleDistance = sp.finity
        self.nearestObstacleAngle = 0
        
        self.nextObstacleDistance = sp.finity
        self.nextObstacleAngle = 0

        self.lidar = sp.world.visualisation.lidar
        
        for lidarAngle in range (-self.lidar.halfApertureAngle, self.lidar.halfApertureAngle):
            lidarDistance = self.lidar.distances [lidarAngle]
            
            if lidarDistance < self.nearestObstacleDistance:
                self.nextObstacleDistance =  self.nearestObstacleDistance
                self.nextObstacleAngle = self.nearestObstacleAngle
                
                self.nearestObstacleDistance = lidarDistance 
                self.nearestObstacleAngle = lidarAngle

            elif lidarDistance < self.nextObstacleDistance:
                self.nextObstacleDistance = lidarDistance
                self.nextObstacleAngle = lidarAngle
           
        self.targetObstacleDistance = (self.nearestObstacleDistance + self.nextObstacleDistance) / 2
        self.targetObstacleAngle = (self.nearestObstacleAngle + self.nextObstacleAngle) / 2
        
    def sweep (self):
        self.steeringAngle = self.targetObstacleAngle
        self.targetVelocity = (sp.abs (90 - self.steeringAngle) / 65) if self.driveEnabled else 0
        
    def output (self):
        sp.world.physics.steeringAngle.set (self.steeringAngle)
        sp.world.physics.targetVelocity.set (self.targetVelocity)
        
