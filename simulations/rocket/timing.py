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

class Timing (Chart):
    def __init__ (self):
        Chart.__init__ (self)
        
    def define (self):
        self.channel (world.rocket.srq0, red, -1, 1, 100)
        self.channel (world.rocket.srq1, green, -1, 1, 100)
        self.channel (world.rocket.srq2, blue, -1, 1, 100)     
        self.channel (world.rocket.srq3, yellow, -1, 1, 100)     
        self.channel (world.rocket.axisX, maroon, -1, 1, 100)
        self.channel (world.rocket.axisY, olive, -1, 1, 100)
        self.channel (world.rocket.axisZ, lime, -1, 1, 100)     
        self.channel (world.rocket.angle, fuchsia, -360, 360, 100)  
                