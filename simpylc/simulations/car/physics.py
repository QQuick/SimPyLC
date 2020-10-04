# ====== Legal notices
#
# Copyright (C) 2013  - 2020 GEATEC engineering
#
# This program is free software./
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

import simpylc as sp

import parameters as pm

class Physics (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('car physics')
        
        self.group ('wheels', True)
        
        self.acceleration = sp.Register (2)
        self.targetVelocity= sp.Register ()
        self.velocity = sp.Register ()
        self.midWheelAngularVelocity = sp.Register ()
        self.midWheelAngle = sp.Register (30)
        
        self.steeringAngle = sp.Register ()
        self.midSteeringAngle = sp.Register ()
        
        self.inverseMidCurveRadius = sp.Register (20)       
        self.midAngularVelocity = sp.Register ()
        
        self.attitudeAngle = sp.Register (50)
        self.courseAngle = sp.Register ()
        
        self.tangentialVelocity = sp.Register ()
        self.velocityX = sp.Register ()
        self.velocityY = sp.Register ()

        self.positionX = sp.Register ()
        self.positionY = sp.Register ()
        
        self.radialAcceleration = sp.Register ()
        self.slipping = sp.Marker ()
        self.radialVelocity = sp.Register ()
        
    def sweep (self):
        self.page ('traction')  
        self.group ('wheels', True)
        
        self.velocity.set (self.velocity + self.acceleration * sp.world.period, self.velocity < self.targetVelocity, self.velocity - self.acceleration * sp.world.period)
        self.midWheelAngularVelocity.set (self.velocity / pm.displacementPerWheelAngle)
        self.midWheelAngle.set (self.midWheelAngle + self.midWheelAngularVelocity * sp.world.period)
        self.tangentialVelocity.set (self.midWheelAngularVelocity * pm.displacementPerWheelAngle) 
        
        self.midSteeringAngle.set (sp.atan (0.5 * sp.tan (self.steeringAngle)))
        
        self.inverseMidCurveRadius.set (sp.sin (self.midSteeringAngle) / pm.wheelShift)
        self.midAngularVelocity.set (sp.degreesPerRadian * self.tangentialVelocity * self.inverseMidCurveRadius) 
        
        self.attitudeAngle.set (self.attitudeAngle + self.midAngularVelocity * sp.world.period)
        self.courseAngle.set (self.attitudeAngle + self.midSteeringAngle)
        
        self.radialAcceleration.set (sp.max (abs (self.tangentialVelocity * self.tangentialVelocity * self.inverseMidCurveRadius) - 0.5, 0))
        self.slipping.mark (sp.abs (self.radialAcceleration) > 0.55)
        self.radialVelocity.set (self.radialVelocity + self.radialAcceleration * sp.world.period, self.slipping, 0)
        
        self.velocityX.set (self.tangentialVelocity * sp.cos (self.courseAngle) + self.radialVelocity * sp.sin (self.courseAngle))
        self.velocityY.set (self.tangentialVelocity * sp.sin (self.courseAngle) + self.radialVelocity * sp.cos (self.courseAngle))
        
        self.positionX.set (self.positionX + self.velocityX * sp.world.period)
        self.positionY.set (self.positionY + self.velocityY * sp.world.period)
        
