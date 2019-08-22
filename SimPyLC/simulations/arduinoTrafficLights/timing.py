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
        self.channel (world.trafficLights.northGreenLamp, green)
        self.channel (world.trafficLights.northRedLamp, red)
        self.channel (world.trafficLights.eastGreenLamp, green)
        self.channel (world.trafficLights.eastRedLamp, red)
        self.channel (world.trafficLights.southGreenLamp, green)
        self.channel (world.trafficLights.southRedLamp, red)
        self.channel (world.trafficLights.westGreenLamp, green)
        self.channel (world.trafficLights.westRedLamp, red)
        self.channel (world.trafficLights.regularPhaseTimer, aqua, 0, 20, 60)
        self.channel (world.trafficLights.cyclePhaseTimer, aqua, 0, 40, 60)
        self.channel (world.trafficLights.blinkTimer, aqua, 0, 0.3, 60)
        self.channel (world.trafficLights.modeButton, white)
        self.channel (world.trafficLights.modePulse, white)
        self.channel (world.trafficLights.modeStep, white, 0, 3, 60)
        self.channel (world.trafficLights.brightButton, yellow)
        self.channel (world.trafficLights.brightPulse, yellow)
        self.channel (world.trafficLights.brightDirection, yellow)
        self.channel (world.trafficLights.streetLamp, yellow, 0, 5000, 60)
        