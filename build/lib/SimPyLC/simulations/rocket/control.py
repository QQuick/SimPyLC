# ====== Legal notices
#
# Copyright (C) 2013 - 2018 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
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

from SimPyLC import *

class Control (Module):
    def __init__ (self):
        Module.__init__ (self)
        
        self.page ('rocket control')
        
        self.group ('gimbal angle controls blue/yellow', True)
        self.toYellow = Marker ()
        self.toBlue = Marker ()
        
        self.group ('gimbal angle state blue/yellow')
        self.blueYellowDelta = Register ()
        self.blueYellowAngle = Register ()
        
        self.group ('thruster angle controls green/red', True)
        self.toRed = Marker ()
        self.toGreen = Marker ()
                
        self.group ('thruster angle state green/red')
        self.greenRedDelta = Register ()
        self.greenRedAngle = Register ()
        
        self.group ('fuel throttle controls', True)
        self.throttleOpen = Marker ()
        self.throttleClose = Marker ()
        
        self.group ('fuel throttle state')
        self.throttleDelta = Register ()
        self.throttlePercent = Register ()
        
    def input (self):
        self.part ('gimbal angle blue/yellow')
        self.blueYellowAngle.set (world.rocket.blueYellowAngle)
        
        self.part ('thruster angle green/red')
        self.greenRedAngle.set (world.rocket.greenRedAngle)
        
        self.part ('fuel throttle')
        self.throttlePercent.set (world.rocket.throttlePercent)
        
    def sweep (self):
        self.part ('gimbal angle blue/yellow')
        self.blueYellowDelta.set (-1 if self.toBlue else 1 if self.toYellow else 0)
        
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (-1 if self.toGreen else 1 if self.toRed else 0)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (-1 if self.throttleClose else 1 if self.throttleOpen else 0)
        
        
        