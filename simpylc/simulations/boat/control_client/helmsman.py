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

import time as tm
import math as mt
import sys as ss
import os

ss.path +=  [os.path.abspath (relPath) for relPath in  ('..',)]

import socket_wrapper as sw
import almanac as an

class Helmsman:
    def __init__ (self, crew):
        self.crew = crew
        self.targetWaypointIndex = 0
        self.exclude = an.Exclude (45)

    def sweep (self):
        try:
            leg = an.getLeg (self.crew.deckhand.getCurrentLocation (), self.crew.captain.waypoints [self.targetWaypointIndex])
            targetAngle = an.getLegAngle (leg)
            targetDistance = an.getLegLength (leg)

            courseAngle = self.crew.deckhand.getCourseAngle ()
            vaneAngle = self.crew.deckhand.getVaneAngle ()
            windAngle = an.symmetrize (vaneAngle + courseAngle)

            heightAngle = an.symmetrize (targetAngle - windAngle)
            sailableHeightAngle = self.exclude (heightAngle)                # Will result in plying automagically if needed
            sailableTargetAngle = an.symmetrize (sailableHeightAngle + windAngle - courseAngle)

            self.crew.deckhand.setRudderAngle (an.clip (-sailableTargetAngle, 45))
            self.crew.deckhand.setSailAngle (an.clip (vaneAngle / 2, 90))   # Chinese gybes allowed

            if targetDistance < 1:
                self.targetWaypointIndex += 1

        except IndexError:                                                  # No more waypoints
            self.crew.deckhand.holdPosition ()

    def sail (self):
        self.crew.deckhand.work (self.sweep)
