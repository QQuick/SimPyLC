# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software./
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

from SimPyLC import *

class Rocket (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.page ('rocket physics')
        
        self.group ('thruster angle green/red', True) 
        self.greenRedDelta = Register ()
        self.greenRedAngle = Register ()
        
        self.group ('thruster angle blue/yellow')
        self.blueYellowDelta = Register ()
        self.blueYellowAngle = Register ()
        
        self.group ('fuel throttle')
        self.throttleDelta = Register ()
        self.throttlePercent = Register ()
        self.thrusterForce = Register ()      
        
        self.group ('ship')
        self.mass = Register (5000)
        self.thrusterTiltSpeed = Register (30)
        self.thrusterMaxAngle = Register (90)
        self.throttleSpeed = Register (20)
        self.thrusterMaxForce = Register (10000)
        
    def input (self):   
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (world.control.greenRedDelta)
        
        self.part ('thruster angle blue/yellow')
        self.blueYellowDelta.set (world.control.blueYellowDelta)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (world.control.throttleDelta)
        
    def sweep (self):
        self.part ('thruster angle green/red')
        self.greenRedAngle.set (
            limit (
                self.greenRedAngle + self.greenRedDelta * self.thrusterTiltSpeed * world.period,
                self.thrusterMaxAngle
            )
        )
        
        self.part ('thruster angle blue/yellow')
        self.blueYellowAngle.set (
            limit (
                self.blueYellowAngle + self.blueYellowDelta * self.thrusterTiltSpeed * world.period,
                self.thrusterMaxAngle
            )
        )
        
        self.part ('fuel throttle')
        self.throttlePercent.set (
            limit (
                self.throttlePercent + self.throttleDelta * self.throttleSpeed * world.period,
                0,
                100
            )
        )
        self.thrusterForce.set (self.throttlePercent * self.thrusterMaxForce / 100)
                
        