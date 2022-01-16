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

import dimensions as dm

class Physics (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('car physics dashboard')
        
        self.group ('wheels', True)
        
        self.acceleration = sp.Register (2)

        self.targetVelocity= sp.Register ()
        self.velocity = sp.Register ()

        self.steeringAngle = sp.Register ()
        
        self.group ('position', True)

        self.attitudeAngle = sp.Register (50)
        self.courseAngle = sp.Register ()

        self.positionX = sp.Register ()
        self.positionY = sp.Register ()
        
        self.group('slip', True)

        self.radialAcceleration = sp.Register ()
        self.slipping = sp.Marker ()

        self.group ('camera')

        self.soccerView = sp.Latch (True)
        self.heliView = sp.Latch ()
        self.driverView = sp.Latch ()

        self.driverFocusDist = sp.Register (2)

        self.page ('car physics internals')

        self.group ('wheels', True)
        
        self.midWheelAngularVelocity = sp.Register ()
        self.midWheelAngle = sp.Register (30)

        self.midSteeringAngle = sp.Register ()
        self.inverseMidCurveRadius = sp.Register (20)       
        self.midAngularVelocity = sp.Register ()
        
        self.group ('position', True)
        
        self.tangentialVelocity = sp.Register ()
        self.velocityX = sp.Register ()
        self.velocityY = sp.Register ()
        
        self.group('slip', True)
        self.radialVelocity = sp.Register ()

        self.group ('camera')

        self.soccerViewOneshot = sp.Oneshot ()
        self.heliViewOneshot = sp.Oneshot ()
        self.driverViewOneshot = sp.Oneshot ()

        self.driverFocusX = sp.Register ()
        self.driverFocusY = sp.Register ()
        
    def sweep (self):
        self.page ('car physics')

        self.group ('speed')
        
        self.velocity.set (self.velocity + self.acceleration * sp.world.period, self.velocity < self.targetVelocity, self.velocity - self.acceleration * sp.world.period)
        self.midWheelAngularVelocity.set (self.velocity / dm.displacementPerWheelAngle)
        self.midWheelAngle.set (self.midWheelAngle + self.midWheelAngularVelocity * sp.world.period)
        self.tangentialVelocity.set (self.midWheelAngularVelocity * dm.displacementPerWheelAngle) 
        
        self.group ('direction')

        self.midSteeringAngle.set (sp.atan (0.5 * sp.tan (self.steeringAngle)))
        
        self.inverseMidCurveRadius.set (sp.sin (self.midSteeringAngle) / dm.wheelShift)
        self.midAngularVelocity.set (sp.degreesPerRadian * self.tangentialVelocity * self.inverseMidCurveRadius) 
        
        self.attitudeAngle.set (self.attitudeAngle + self.midAngularVelocity * sp.world.period)
        self.courseAngle.set (self.attitudeAngle + self.midSteeringAngle)
        
        self.radialAcceleration.set (sp.max (abs (self.tangentialVelocity * self.tangentialVelocity * self.inverseMidCurveRadius) - 0.5, 0))
        self.slipping.mark (sp.abs (self.radialAcceleration) > 0.55)
        self.radialVelocity.set (self.radialVelocity + self.radialAcceleration * sp.world.period, self.slipping, 0)
        
        self.velocityX.set (self.tangentialVelocity * sp.cos (self.courseAngle) + self.radialVelocity * sp.sin (self.courseAngle))
        self.velocityY.set (self.tangentialVelocity * sp.sin (self.courseAngle) + self.radialVelocity * sp.cos (self.courseAngle))
        
        self.group ('position')

        self.positionX.set (self.positionX + self.velocityX * sp.world.period)
        self.positionY.set (self.positionY + self.velocityY * sp.world.period)

        self.group ('camera')

        self.soccerView.unlatch (self.heliViewOneshot or self.driverViewOneshot)
        self.heliView.unlatch (self.soccerViewOneshot or self.driverViewOneshot)
        self.driverView.unlatch (self.soccerViewOneshot or self.heliViewOneshot)

        self.soccerViewOneshot.trigger (self.soccerView)
        self.heliViewOneshot.trigger (self.heliView)
        self.driverViewOneshot.trigger (self.driverView)
        
        self.driverFocusX.set (self.positionX + self.driverFocusDist * sp.cos (self.attitudeAngle))
        self.driverFocusY.set (self.positionY + self.driverFocusDist * sp.sin (self.attitudeAngle))
        