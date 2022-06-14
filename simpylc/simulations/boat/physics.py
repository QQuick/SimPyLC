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

        self.page ('boat physics, units: m s °')

        self.group ('environment', True)

        self.windAngle = sp.Register ()
        self.windSpeed = sp.Register ()

        self.streamAngle = sp.Register ()
        self.streamSpeed = sp.Register ()

        self.group ('sensors')

        self.courseAngle = sp.Register ()
        self.tiltAngle = sp.Register ()
        self.vaneAngle = sp.Register ()

        self.positionX = sp.Register ()
        self.positionY = sp.Register ()

        self.group ('actuators')

        self.rudderAngle = sp.Register ()
        self.sheetLength = sp.Register ()

        self.group ('boat parameters')
        self.sailFactor = sp.Register (1)
        self.tiltFactor = sp.Register (1)
        self.dragFactor = sp.Register (1)

        self.group ('camera')

        self.soccerView = sp.Latch (True)
        self.soccerDist = sp.Register (3)

        self.heliView = sp.Latch ()
        self.heliDist = sp.Register (10)

        self.helmsmanView = sp.Latch ()
        self.helmsmanDist = sp.Register (2)

        self.group ('dynamics', True)

        self.vaneSign = sp.Register ()
        self.absSailAngle = sp.Register ()
        self.sailAngle = sp.Register ()
        self.attackAngle = sp.Register ()
        self.sailForce = sp.Register ()
        self.forwardForce = sp.Register ()
        self.driftForce = sp.Register ()
        self.dragForce = sp.Register ()

        self.group ('kinematics')

        self.acceleration = sp.Register ()

        self.velocity = sp.Register ()
        self.velocityX = sp.Register ()
        self.velocityY = sp.Register ()

        self.group ('optics')

        self.soccerViewOneshot = sp.Oneshot ()
        self.heliViewOneshot = sp.Oneshot ()
        self.helmsmanViewOneshot = sp.Oneshot ()

        self.helmsmanFocusX = sp.Register ()
        self.helmsmanFocusY = sp.Register ()

    def sweep (self):
        self.page ('boat physics')

        self.group ('dynamics')

        self.vaneAngle.set (sp.sym (self.windAngle - self.courseAngle))
        self.vaneSign.set (1, self.vaneAngle > 0, -1)
        self.absSailAngle.set (sp.min (2 * sp.atan2 (self.sheetLength / 2, dm.boomLength), sp.abs (self.vaneAngle), 90))  # 1 isosceles triangle == 2 right angled triangles
        self.sailAngle.set (self.absSailAngle, self.vaneAngle > 0, -self.absSailAngle)
        self.attackAngle.set (self.sailAngle - self.vaneAngle)

        self.sailForce.set (self.sailFactor * self.windSpeed * sp.sin (self.attackAngle) * sp.cos (self.tiltAngle))
        self.forwardForce.set (self.sailForce * sp.sin (self.absSailAngle))
        self.driftForce.set (self.vaneSign * self.sailForce * sp.cos (self.absSailAngle))
        self.tiltAngle.set (self.tiltFactor * self.driftForce)
        self.dragForce.set (self.dragFactor * sp.pow (self.velocity, 2))  # Rudder angle neglected for now

        self.group ('kinematics')

        self.acceleration.set (self.forwardForce - self.dragForce)
        self.velocity.set (self.velocity + self.acceleration * sp.world.period)

        self.velocityX.set (self.velocity * sp.cos (self.courseAngle))
        self.velocityY.set (self.velocity * sp.sin (self.courseAngle))

        self.positionX.set (self.positionX + self.velocityX * sp.world.period)
        self.positionY.set (self.positionY + self.velocityY * sp.world.period)

        self.group ('camera')

        self.soccerView.unlatch (self.heliViewOneshot or self.helmsmanViewOneshot)
        self.heliView.unlatch (self.soccerViewOneshot or self.helmsmanViewOneshot)
        self.helmsmanView.unlatch (self.soccerViewOneshot or self.heliViewOneshot)

        self.soccerViewOneshot.trigger (self.soccerView)
        self.heliViewOneshot.trigger (self.heliView)
        self.helmsmanViewOneshot.trigger (self.helmsmanView)

        self.helmsmanFocusX.set (self.positionX + self.helmsmanDist * sp.cos (self.courseAngle))
        self.helmsmanFocusY.set (self.positionY + self.helmsmanDist * sp.sin (self.courseAngle))

