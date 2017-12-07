# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software./
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

class Rocket (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.page ('rocket physics')
        
        self.group ('thruster', True)
        self.greenRed = Register ()
        self.blueYellow = Register ()
        self.force = Register ()
        
        self.group ('ship')
        self.mass = Register ()
        
    def input (self):   
        self.part ('thruster control')
        self.greenRed.set (world.control.greenRed)
        self.blueYellow.set (world.control.blueYellow)
        self.force.set (world.control.force)
        
    def sweep (self):
        pass
        #self.part ('Torso')
        #self.torTorq.set (limit (self.torGain * self.torVolt, self.torMax), self.torEnab, 0)
        
        