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

class Physics (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('train physics')
        
        self.group ('control signals', True)
        self.brakeLift = sp.Marker ()
        self.driveEnable = sp.Marker ()
    
        self.group ('state')
        self.targetAccel = sp.Register ()
        self.speed = sp.Register ()
        self.position = sp.Register ()

        self.group ('limits', True)
        self.maxBrakeDecel = sp.Register (5)
        self.maxDriveAccel= sp.Register (2)
        self.maxDriveDecel = sp.Register (3)
        self.maxSpeed = sp.Register (30)
        self.maxPosition = sp.Register (20_000)

        self.group ('auxiliary')
        self.brakeAccel = sp.Register ()
        self.driveAccel = sp.Register ()
        
    def sweep (self):
        self.part ('acceleration')
        self.brakeAccel.set (0, self.brakeLift, -self.maxBrakeDecel)
        self.driveAccel.set (self.maxDriveAccel, self.driveEnable, -self.maxDriveDecel)
        self.targetAccel.set (self.brakeAccel + self.driveAccel)

        self.part ('integration')
        self.speed.set (sp.limit (self.speed + self.targetAccel * sp.world.period, 0, self.maxSpeed))
        self.position.set (self.position + self.speed * sp.world.period)
        