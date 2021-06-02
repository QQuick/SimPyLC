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

class Control (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        
        self.page ('rocket control')
        
        self.group ('gimbal angle controls blue/yellow', True)
        self.toYellow = sp.Marker ()
        self.toBlue = sp.Marker ()
        
        self.group ('gimbal angle state blue/yellow')
        self.blueYellowDelta = sp.Register ()
        self.blueYellowAngle = sp.Register ()
        
        self.group ('thruster angle controls green/red', True)
        self.toRed = sp.Marker ()
        self.toGreen = sp.Marker ()
                
        self.group ('thruster angle state green/red')
        self.greenRedDelta = sp.Register ()
        self.greenRedAngle = sp.Register ()
        
        self.group ('fuel throttle controls', True)
        self.throttleOpen = sp.Marker ()
        self.throttleClose = sp.Marker ()
        
        self.group ('fuel throttle state')
        self.throttleDelta = sp.Register ()
        self.throttlePercent = sp.Register ()
        
    def input (self):
        self.part ('gimbal angle blue/yellow')
        self.blueYellowAngle.set (sp.world.rocket.blueYellowAngle)
        
        self.part ('thruster angle green/red')
        self.greenRedAngle.set (sp.world.rocket.greenRedAngle)
        
        self.part ('fuel throttle')
        self.throttlePercent.set (sp.world.rocket.throttlePercent)
        
    def sweep (self):
        self.part ('gimbal angle blue/yellow')
        self.blueYellowDelta.set (-1 if self.toBlue else 1 if self.toYellow else 0)
        
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (-1 if self.toGreen else 1 if self.toRed else 0)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (-1 if self.throttleClose else 1 if self.throttleOpen else 0)
        
        
        
