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

class Timing (sp.Chart):
    def __init__ (self):
        sp.Chart.__init__ (self)
        
    def define (self):
        self.channel (sp.world.control.brakeLiftButton, sp.lime)
        self.channel (sp.world.control.driveEnableButton, sp.lime)

        self.channel (sp.world.control.brakeWarnLamp, sp.red)
        self.channel (sp.world.control.speedWarnLamp, sp.red)

        self.channel (sp.world.physics.targetAccel, sp.yellow, -10, 5, 100)

        self.channel (sp.world.control.speed, sp.white, 0, 50, 200)
        self.channel (sp.world.control.accel, sp.white, -10, 5, 100)
