# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
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

import simpylc as sp

class Timing (sp.Chart):
    def __init__ (self):
        sp.Chart.__init__ (self)
        
    def define (self):
        self.channel (sp.world.control.digitIndex, sp.olive, 0, 3, 40)
        self.channel (sp.world.control.digitValue, sp.olive)
        self.channel (sp.world.control.digitDot, sp.olive, 0, 3, 40)
        self.channel (sp.world.control.buzzerPitchTimer, sp.aqua, 0, 1, 40)
        self.channel (sp.world.control.buzzer, sp.aqua)
        self.channel (sp.world.control.upButton, sp.red)
        self.channel (sp.world.control.downButton, sp.red)
        self.channel (sp.world.control.plateSelectNr, sp.red, 0, 3, 40)
        self.channel (sp.world.control.alarmTimeLeft, sp.green, 0, 300, 90)
        
