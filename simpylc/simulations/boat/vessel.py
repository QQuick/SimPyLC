'''
====== Legal notices

Copyright (C) 2013 - 2022 GEATEC engineering

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

import sys as ss

ss.path.append ('./control_client')

import simpylc as sp

import constants as cs
import almanac as an

waypoints = an.getWaypoints ()

class Vessel (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('State [m, s, °]')

        self.group ('Environment', True)

        self.windAngle = sp.Register (135)  # SW
        self.windSpeed = sp.Register ()

        self.group ('Actuators')

        self.rudderAngle = sp.Register ()
        self.sheetLength = sp.Register (sp.finity)

        self.group ('Sensors')

        self.courseAngle = sp.Register ()
        self.vaneAngle = sp.Register ()

        self.lattitude = sp.Register (waypoints [0][0])
        self.longitude = sp.Register (waypoints [0][1])

        self.group ('Kinematics', True)

        self.acceleration = sp.Register ()
        self.velocity = sp.Register ()

        self.group ('Camera')

        self.soccerView = sp.Latch (True)
        self.heliView = sp.Latch ()
        self.helmsmanView = sp.Latch ()

        self.page ('Internals [m, s, °]')

        self.group ('Dynamics settings', True)

        self.boatMass = sp.Register (10)
        self.sailFactor = sp.Register (3)
        self.rudderFactor = sp.Register (1)
        self.dragFactor = sp.Register (2)

        self.group ('Dynamics helpers')

        self.carthesianAngle = sp.Register ()
        self.absSailAngle = sp.Register ()
        self.sailAngle = sp.Register ()
        self.attackAngle = sp.Register ()
        self.sailForce = sp.Register ()
        self.forwardForce = sp.Register ()
        self.dragForce = sp.Register ()

        self.group ('Kinematics helpers', True)

        self.velocityX = sp.Register ()
        self.velocityY = sp.Register ()

        self.group ('Camera settings')

        self.soccerFocusDist = sp.Register (9)
        self.heliFocusDist = sp.Register (30)
        self.helmsmanFocusDist = sp.Register (6)

        self.group ('Camera helpers')

        self.helmsmanFocusDistX = sp.Register ()
        self.helmsmanFocusDistY = sp.Register ()

        self.soccerViewOneshot = sp.Oneshot ()
        self.heliViewOneshot = sp.Oneshot ()
        self.helmsmanViewOneshot = sp.Oneshot ()

    def sweep (self):
        self.page ('Boat physics')

        self.group ('Dynamics')

        self.courseAngle.set (sp.sym (self.courseAngle - self.rudderFactor * self.rudderAngle * self.velocity / self.boatMass))
        self.carthesianAngle.set (sp.asym (self.courseAngle + 90))
        self.vaneAngle.set (sp.sym (self.windAngle - self.courseAngle))

        try:
            self.absSailAngle.set (sp.min (2 * sp.asin (0.5 * self.sheetLength / cs.boomLength), sp.abs (self.vaneAngle), 90))  # 1 isosceles triangle == 2 right angled triangles
        except ValueError:  # Sheetlength too large, assume hold position
            self.absSailAngle.set (sp.abs (self.vaneAngle))

        self.sailAngle.set (self.absSailAngle if self.vaneAngle >= 0 else -self.absSailAngle)
        self.attackAngle.set (self.vaneAngle - self.sailAngle)

        self.sailForce.set (self.sailFactor * self.windSpeed * sp.sin (self.attackAngle))
        self.forwardForce.set (self.sailForce * sp.sin (self.sailAngle))
        self.dragForce.set (self.dragFactor * sp.pow (self.velocity, 2))

        self.group ('Kinematics')

        self.acceleration.set ((self.forwardForce - self.dragForce) / self.boatMass)
        self.velocity.set (self.velocity + self.acceleration * sp.world.period)

        self.velocityX.set (self.velocity * sp.cos (self.carthesianAngle))
        self.velocityY.set (self.velocity * sp.sin (self.carthesianAngle))

        lattitude, longitude = an.getPosition (sp.tEva ((self.lattitude, self.longitude)), (self.velocityX, self.velocityY), sp.world.period)
        self.lattitude.set (lattitude)
        self.longitude.set (longitude)

        self.group ('Camera')

        self.soccerView.unlatch (self.heliViewOneshot or self.helmsmanViewOneshot)
        self.heliView.unlatch (self.soccerViewOneshot or self.helmsmanViewOneshot)
        self.helmsmanView.unlatch (self.soccerViewOneshot or self.heliViewOneshot)

        self.soccerViewOneshot.trigger (self.soccerView)
        self.heliViewOneshot.trigger (self.heliView)
        self.helmsmanViewOneshot.trigger (self.helmsmanView)

        self.helmsmanFocusDistX.set (self.helmsmanFocusDist * sp.cos (self.carthesianAngle))
        self.helmsmanFocusDistY.set (self.helmsmanFocusDist * sp.sin (self.carthesianAngle))

