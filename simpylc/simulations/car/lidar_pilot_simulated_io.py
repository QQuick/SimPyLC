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

import simpylc as sp
import lidar_pilot_base as lb

class LidarPilotSimulatedIo (lb.LidarPilotBase):
    def __init__ (self):
        print ('Use up arrow to start, down arrow to stop')
        self.finity = sp.finity
        super () .__init__ ()
        
    def input (self):   # Input from simulator
        super () .input ()
        key = sp.getKey ()
        
        if key == 'KEY_UP':
            self.driveEnabled = True
        elif key == 'KEY_DOWN':
            self.driveEnabled = False
        
        self.lidarDistances = sp.world.visualisation.lidar.distances
        self.lidarHalfApertureAngle = sp.world.visualisation.lidar.halfApertureAngle
        
    def output (self):  # Output to simulator
        super () .output ()
        sp.world.physics.steeringAngle.set (self.steeringAngle)
        sp.world.physics.targetVelocity.set (self.targetVelocity)
        
