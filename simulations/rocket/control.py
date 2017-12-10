# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
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

class Control (Module):
    def __init__ (self):
        Module.__init__ (self)
        
        self.page ('rocket control')
        
        self.group ('thruster angle green/red', True)
        self.toGreen = Marker ()
        self.toRed = Marker ()
        self.greenRedDelta = Register ()
        self.greenRedAngle = Register ()
        
        self.group ('thruster angle blue/yellow')
        self.toBlue = Marker ()
        self.toYellow = Marker ()
        self.blueYellowDelta = Register ()
        self.blueYellowAngle = Register ()
        
        self.group ('fuel throttle')
        self.throttleClose = Marker ()
        self.throttleOpen = Marker ()
        self.throttleDelta = Register ()
        self.throttlePercent = Register ()
        
    def input (self):
        self.part ('thruster angle green/red')
        self.greenRedAngle = world.rocket.greenRedAngle
        
        self.part ('thruster angle blue/yellow')
        self.blueYellowAngle = world.rocket.blueYellowAngle
        
        self.part ('fuel throttle')
        self.throttlePercent = world.rocket.throttlePercent
        
    def sweep (self):
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (-1 if self.toGreen else 1 if self.toRed else 0)
        
        self.part ('thruster angle blue/yellow')
        self.blueYellowDelta.set (-1 if self.toBlue else 1 if self.toYellow else 0)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (-1 if self.throttleClose else 1 if self.throttleOpen else 0)
        
        
        