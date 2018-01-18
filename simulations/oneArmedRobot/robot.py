# ====== Legal notices
#
# Copyright (C) 2013  - 2018 GEATEC engineering
#
# This program is free software./
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

class Robot (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.page ('robot physics')
        
        self.group ('torso electronics', True)
        self.torVolt = Register ()
        self.torEnab = Marker ()
        self.torGain = Register (2)
        self.torMax = Register (20)
    
        self.group ('torso mechanics')
        self.torInert = Register (8)
        self.torTorq = Register ()
        self.torBrake = Marker ()
        self.torAccel = Register ()
        self.torSpeed = Register ()
        self.torAng = Register ()       
        
        self.group ('upper arm electronics', True)
        self.uppVolt = Register ()
        self.uppEnab = Marker ()
        self.uppGain = Register (2)
        self.uppMax = Register (20)
    
        self.group ('upper arm mechanics')
        self.uppInert = Register (4)
        self.uppTorq = Register ()
        self.uppBrake = Marker ()
        self.uppAccel = Register ()
        self.uppSpeed = Register ()
        self.uppAng = Register ()       
        
        self.group ('fore arm electronics', True)
        self.forVolt = Register ()
        self.forEnab = Marker ()
        self.forGain = Register (2)
        self.forMax = Register (20)
    
        self.group ('fore arm mechanics')
        self.forInert = Register (2)
        self.forTorq = Register ()
        self.forBrake = Marker ()
        self.forAccel = Register ()
        self.forSpeed = Register ()
        self.forAng = Register ()
        self.forShift = Register ()
        
        self.group ('wrist electronics', True)
        self.wriVolt = Register ()
        self.wriEnab = Marker ()
        self.wriGain = Register (2)
        self.wriMax = Register (20)
    
        self.group ('wrist mechanics')
        self.wriInert = Register (1)
        self.wriTorq = Register ()
        self.wriBrake = Marker ()
        self.wriAccel = Register ()
        self.wriSpeed = Register ()
        self.wriAng = Register ()
        
        self.group ('hand and finger servos', True)
        self.hanAngSet = Register ()
        self.hanAng = Register ()
        self.hanEnab = Marker ()
        self.finAngSet = Register ()
        self.finAng = Register ()
        self.finEnab = Marker ()
        
    def input (self):   
        self.part ('torso')
        self.torVolt.set (world.control.torVolt)
        self.torEnab.mark (world.control.torEnab)
    
        self.part ('upper arm')
        self.uppVolt.set (world.control.uppVolt)
        self.uppEnab.mark (world.control.uppEnab)

        self.part ('fore arm')
        self.forVolt.set (world.control.forVolt)
        self.forEnab.mark (world.control.forEnab)

        self.part ('wrist')
        self.wriVolt.set (world.control.wriVolt)
        self.wriEnab.mark (world.control.wriEnab)
        
        self.part ('hand and fingers')
        self.hanAngSet.set (world.control.hanAngSet)
        self.hanEnab.mark (world.control.hanEnab)
        self.finAngSet.set (world.control.finAngSet)
        self.finEnab.mark (world.control.finEnab)
        
    def sweep (self):
        self.part ('Torso')
        self.torTorq.set (limit (self.torGain * self.torVolt, self.torMax), self.torEnab, 0)
        self.torBrake.mark (not self.torEnab)
        self.torAccel.set (self.torSpeed / -world.period, self.torBrake, self.torTorq / self.torInert)
        self.torSpeed.set (self.torSpeed + self.torAccel * world.period)
        self.torAng.set (self.torAng + self.torSpeed * world.period)
        
        self.part ('upper arm')
        self.uppTorq.set (limit (self.uppGain * self.uppVolt, self.uppMax), self.uppEnab, 0)
        self.uppBrake.mark (not self.uppEnab)
        self.uppAccel.set (self.uppSpeed / -world.period, self.uppBrake, self.uppTorq / self.uppInert)
        self.uppSpeed.set (self.uppSpeed + self.uppAccel * world.period)
        self.uppAng.set (self.uppAng + self.uppSpeed * world.period)
        
        self.part ('fore arm')
        self.forTorq.set (limit (self.forGain * self.forVolt, self.forMax), self.forEnab, 0)
        self.forBrake.mark (not self.forEnab)
        self.forAccel.set (self.forSpeed / -world.period, self.forBrake, self.forTorq / self.forInert)
        self.forSpeed.set (self.forSpeed + self.forAccel * world.period)
        self.forAng.set (self.forAng + self.forSpeed * world.period)
        
        self.part ('wrist')
        self.wriTorq.set (limit (self.wriGain * self.wriVolt, self.wriMax), self.wriEnab, 0)
        self.wriBrake.mark (not self.wriEnab)
        self.wriAccel.set (self.wriSpeed / -world.period, self.wriBrake, self.wriTorq / self.wriInert)
        self.wriSpeed.set (self.wriSpeed + self.wriAccel * world.period)
        self.wriAng.set (self.wriAng + self.wriSpeed * world.period)
        
        self.part ('hand and fingers')
        self.hanAng.set (self.hanAngSet, self.hanEnab)
        self.finAng.set (self.finAngSet, self.finEnab)
        
        