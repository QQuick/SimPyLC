# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

import simpylc as sp

import parameters as pm

class LidarPilotSp (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('lidar control')
        
        self.group ('inputs', True)

        self.driveEnabled = sp.Marker ()

        self.nearestObstacleDistance = sp.Register (sp.finity)
        self.nearestObstacleAngle = sp.Register (0)

        self.nextObstacleDistance = sp.Register (sp.finity)
        self.nextObstacleAngle = sp.Register (0)

        self.targetObstacleDistance = sp.Register (sp.finity)
        self.targetObstacleAngle = sp.Register (0)

        self.velocity = sp.Register (0)

        self.group ('outputs')
        
        self.targetVelocity = sp.Register ()
        self.steeringAngle = sp.Register (30)

    def input (self):
        self.nearestObstacleDistance.set (sp.finity)
        self.nearestObstacleAngle.set (0)
        
        self.nextObstacleDistance.set (sp.finity)
        self.nextObstacleAngle.set (0)
        
        lidar = sp.world.visualisation.lidar
        
        for lidarAngle in range (-lidar.halfApertureAngle, lidar.halfApertureAngle):
            lidarDistance = lidar.distances [lidarAngle]
            
            if lidarDistance < self.nearestObstacleDistance:
                self.nextObstacleDistance.set (self.nearestObstacleDistance)
                self.nextObstacleAngle.set (self.nearestObstacleAngle)
                
                self.nearestObstacleDistance.set (lidarDistance)
                self.nearestObstacleAngle.set (lidarAngle)

            elif lidarDistance < self.nextObstacleDistance:
                self.nextObstacleDistance.set (lidarDistance)
                self.nextObstacleAngle.set (lidarAngle)
           
        self.targetObstacleDistance.set ((self.nearestObstacleDistance + self.nextObstacleDistance) / 2)
        self.targetObstacleAngle.set ((self.nearestObstacleAngle + self.nextObstacleAngle) / 2)
        
        self.velocity.set (sp.world.physics.velocity)      
        
    def sweep (self):
        self.steeringAngle.set (self.targetObstacleAngle)
        self.targetVelocity.set (sp.abs (90 - self.steeringAngle) / 65, self.driveEnabled, 0)

    def output (self):
        sp.world.physics.steeringAngle.set (self.steeringAngle)
        sp.world.physics.targetVelocity.set (self.targetVelocity)
        
