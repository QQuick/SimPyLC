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

import common as cm

class Timing (sp.Chart):
    def __init__ (self):
        sp.Chart.__init__ (self)
        
    def define (self):
        '''
        if useQuaternions:
            self.channel (sp.world.rocket.shipRotQuat0, sp.white, -1, 1, 100)
            self.channel (sp.world.rocket.shipRotQuat1, sp.white, -1, 1, 100)
            self.channel (sp.world.rocket.shipRotQuat2, sp.white, -1, 1, 100)     
            self.channel (sp.world.rocket.shipRotQuat3, sp.white, -1, 1, 100)
        '''
        
        self.channel (sp.world.rocket.attitudeX, sp.red, -180, 180, 100)
        self.channel (sp.world.rocket.attitudeY, sp.green, -180, 180, 100)
        self.channel (sp.world.rocket.attitudeZ, sp.blue, -180, 180, 100)
        
