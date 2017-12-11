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
        
        self.group ('gimbal angle blue/yellow', True)
        self.blueYellowDelta = Register ()
        self.blueYellowRoughAngle = Register ()
        self.blueYellowAngle = Register ()
        
        self.group ('thruster angle green/red') 
        self.greenRedDelta = Register ()
        self.greenRedRoughAngle = Register ()
        self.greenRedAngle = Register ()
        
        self.group ('fuel throttle')
        self.throttleDelta = Register ()
        self.throttlePercent = Register ()
        self.thrusterForce = Register ()      
        
        self.group ('ship')
        self.shipMass = Register (5000)
        self.thrusterTiltSpeed = Register (30)
        self.thrusterMaxAngle = Register (90)
        self.throttleSpeed = Register (20)
        self.thrusterMaxForce = Register (10000)
        
        self.group ('linear accelleration', True)
        self.linAccelX = Register ()
        self.linAccelY = Register ()
        self.linAccelZ = Register ()
        
        self.group ('linear velocity')
        self.linVelocX = Register ()
        self.linVelocY = Register ()
        self.linVelocZ = Register ()
        
        self.group ('position')
        self.positionX = Register ()
        self.positionY = Register ()
        self.positionZ = Register ()
        
        self.group ('angular acceleration', True)
        self.angAccelX = Register ()
        self.angAccelY = Register ()
        self.angAccelZ = Register ()
        
        self.group ('angular velocity')
        self.angVelocX = Register ()
        self.angVelocY = Register ()
        self.angVelocZ = Register ()
        
        self.group ('attitude')
        self.attitudeX = Register ()
        self.attitudeY = Register ()
        self.attitudeZ = Register ()
        
        self.page ('Forces')
        
        self.group ('Forces w.r.t. ship', True)
        self.forwardForce = Register ()
        self.blueYellowForce = Register ()
        self.greenRedForce = Register ()
        
        self.group ('Forces w.r.t. world')
        self.forceX = Register ()
        self.forceY = Register ()
        self.forceZ = Register ()
        
    def input (self):   
        self.part ('gimbal angle blue/yellow')
        self.blueYellowDelta.set (world.control.blueYellowDelta)
        
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (world.control.greenRedDelta)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (world.control.throttleDelta)
        
    def sweep (self):        
        self.part ('gimbal angle blue/yellow')
        self.blueYellowRoughAngle.set (
            limit (
                self.blueYellowRoughAngle + self.blueYellowDelta * self.thrusterTiltSpeed * world.period,
                self.thrusterMaxAngle
            )
        )
        self.blueYellowAngle.set (snap (self.blueYellowRoughAngle, 0, 3))

        self.part ('thruster angle green/red')
        self.greenRedRoughAngle.set (
            limit (
                self.greenRedRoughAngle + self.greenRedDelta * self.thrusterTiltSpeed * world.period,
                self.thrusterMaxAngle
            )
        )
        self.greenRedAngle.set (snap (self.greenRedRoughAngle, 0, 3))
        
        self.part ('fuel throttle')
        self.throttlePercent.set (
            limit (
                self.throttlePercent + self.throttleDelta * self.throttleSpeed * world.period,
                0,
                100
            )
        )
        self.thrusterForce.set (self.throttlePercent * self.thrusterMaxForce / 100)
        
        
        
        self.part ('dynamics')
        
        
        self.part ('kinematics')

        self.forwardForce.set (self.thrusterForce * cos (self.blueYellowAngle) * cos (self.greenRedAngle))
        self.blueYellowForce.set (self.thrusterForce * sin (self.blueYellowAngle) * cos (self.greenRedAngle))
        self.greenRedForce.set (self.thrusterForce * sin (self.greenRedAngle) * cos (self.blueYellowAngle))
                
        self.linAccelX.set (self.forceX / self.shipMass)
        self.linAccelY.set (self.forceY / self.shipMass)
        self.linAccelZ.set (self.forceZ / self.shipMass)
        
        self.linVelocX.set (self.linVelocX + self.linAccelX * world.period)
        self.linVelocY.set (self.linVelocY + self.linAccelY * world.period)
        self.linVelocZ.set (self.linVelocZ + self.linAccelZ * world.period)
        
        self.positionX.set (self.positionX + self.linVelocX * world.period)
        self.positionY.set (self.positionY + self.linVelocY * world.period)
        self.positionZ.set (self.positionZ + self.linVelocZ * world.period)
        
        
                
        