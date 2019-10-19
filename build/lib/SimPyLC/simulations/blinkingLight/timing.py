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

class Timing (Chart):
    def __init__ (self):
        Chart.__init__ (self)
        
    def define (self):
        self.channel (world.blinkingLight.blinkingTimer, red, 0, 12, 50)
        self.channel (world.blinkingLight.blinkingLight, lime, 0, 1, 50)
        self.channel (world.blinkingLight.pulse, blue, 0, 1, 50)
        self.channel (world.blinkingLight.counter, yellow, 0, 20, 100)
        