# ====== Legal notices
#
# Copyright (C) 2013  - 2018 GEATEC engineering
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
        self.channel (world.robot.torEnab, white)
        self.channel (world.robot.torVolt, red, -10, 10, 20)
        self.channel (world.robot.torAng, red, -220, 220, 70)
        self.channel (world.robot.torBrake, red)
        
        self.channel (world.robot.uppEnab, white)
        self.channel (world.robot.uppVolt, lime, -10, 10, 20)
        self.channel (world.robot.uppAng, lime, -110, 110, 35)
        self.channel (world.robot.uppBrake, lime)
        
        self.channel (world.robot.forEnab, white)
        self.channel (world.robot.forVolt, blue, -10, 10, 20)
        self.channel (world.robot.forAng, blue, -110, 110, 35)
        self.channel (world.robot.forBrake, blue)

        self.channel (world.robot.wriEnab, white)
        self.channel (world.robot.wriVolt, yellow, -10, 10, 20)
        self.channel (world.robot.wriAng, yellow, -110, 110, 35)
        self.channel (world.robot.wriBrake, yellow)
        
        self.channel (world.robot.hanEnab, white)
        self.channel (world.robot.hanAng, aqua, -110, 110, 35)
        
        self.channel (world.robot.finEnab, white)
        self.channel (world.robot.finAng, fuchsia, -55, 55, 35)
        
                