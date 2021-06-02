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

import simpylc as sp

class Robot (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('robot physics')
        
        self.group ('torso electronics', True)
        self.torVolt = sp.Register ()
        self.torEnab = sp.Marker ()
        self.torGain = sp.Register (2)
        self.torMax = sp.Register (20)
    
        self.group ('torso mechanics')
        self.torInert = sp.Register (8)
        self.torTorq = sp.Register ()
        self.torBrake = sp.Marker ()
        self.torAccel = sp.Register ()
        self.torSpeed = sp.Register ()
        self.torAng = sp.Register ()       
        
        self.group ('upper arm electronics', True)
        self.uppVolt = sp.Register ()
        self.uppEnab = sp.Marker ()
        self.uppGain = sp.Register (2)
        self.uppMax = sp.Register (20)
    
        self.group ('upper arm mechanics')
        self.uppInert = sp.Register (4)
        self.uppTorq = sp.Register ()
        self.uppBrake = sp.Marker ()
        self.uppAccel = sp.Register ()
        self.uppSpeed = sp.Register ()
        self.uppAng = sp.Register ()       
        
        self.group ('fore arm electronics', True)
        self.forVolt = sp.Register ()
        self.forEnab = sp.Marker ()
        self.forGain = sp.Register (2)
        self.forMax = sp.Register (20)
    
        self.group ('fore arm mechanics')
        self.forInert = sp.Register (2)
        self.forTorq = sp.Register ()
        self.forBrake = sp.Marker ()
        self.forAccel = sp.Register ()
        self.forSpeed = sp.Register ()
        self.forAng = sp.Register ()
        self.forShift = sp.Register ()
        
        self.group ('wrist electronics', True)
        self.wriVolt = sp.Register ()
        self.wriEnab = sp.Marker ()
        self.wriGain = sp.Register (2)
        self.wriMax = sp.Register (20)
    
        self.group ('wrist mechanics')
        self.wriInert = sp.Register (1)
        self.wriTorq = sp.Register ()
        self.wriBrake = sp.Marker ()
        self.wriAccel = sp.Register ()
        self.wriSpeed = sp.Register ()
        self.wriAng = sp.Register ()
        
        self.group ('hand and finger servos', True)
        self.hanAngSet = sp.Register ()
        self.hanAng = sp.Register ()
        self.hanEnab = sp.Marker ()
        self.finAngSet = sp.Register ()
        self.finAng = sp.Register ()
        self.finEnab = sp.Marker ()
        
    def input (self):   
        self.part ('torso')
        self.torVolt.set (sp.world.control.torVolt)
        self.torEnab.mark (sp.world.control.torEnab)
    
        self.part ('upper arm')
        self.uppVolt.set (sp.world.control.uppVolt)
        self.uppEnab.mark (sp.world.control.uppEnab)

        self.part ('fore arm')
        self.forVolt.set (sp.world.control.forVolt)
        self.forEnab.mark (sp.world.control.forEnab)

        self.part ('wrist')
        self.wriVolt.set (sp.world.control.wriVolt)
        self.wriEnab.mark (sp.world.control.wriEnab)
        
        self.part ('hand and fingers')
        self.hanAngSet.set (sp.world.control.hanAngSet)
        self.hanEnab.mark (sp.world.control.hanEnab)
        self.finAngSet.set (sp.world.control.finAngSet)
        self.finEnab.mark (sp.world.control.finEnab)
        
    def sweep (self):
        self.part ('Torso')
        self.torTorq.set (sp.limit (self.torGain * self.torVolt, self.torMax), self.torEnab, 0)
        self.torBrake.mark (not self.torEnab)
        self.torAccel.set (self.torSpeed / -sp.world.period, self.torBrake, self.torTorq / self.torInert)
        self.torSpeed.set (self.torSpeed + self.torAccel * sp.world.period)
        self.torAng.set (self.torAng + self.torSpeed * sp.world.period)
        
        self.part ('upper arm')
        self.uppTorq.set (sp.limit (self.uppGain * self.uppVolt, self.uppMax), self.uppEnab, 0)
        self.uppBrake.mark (not self.uppEnab)
        self.uppAccel.set (self.uppSpeed / -sp.world.period, self.uppBrake, self.uppTorq / self.uppInert)
        self.uppSpeed.set (self.uppSpeed + self.uppAccel * sp.world.period)
        self.uppAng.set (self.uppAng + self.uppSpeed * sp.world.period)
        
        self.part ('fore arm')
        self.forTorq.set (sp.limit (self.forGain * self.forVolt, self.forMax), self.forEnab, 0)
        self.forBrake.mark (not self.forEnab)
        self.forAccel.set (self.forSpeed / -sp.world.period, self.forBrake, self.forTorq / self.forInert)
        self.forSpeed.set (self.forSpeed + self.forAccel * sp.world.period)
        self.forAng.set (self.forAng + self.forSpeed * sp.world.period)
        
        self.part ('wrist')
        self.wriTorq.set (sp.limit (self.wriGain * self.wriVolt, self.wriMax), self.wriEnab, 0)
        self.wriBrake.mark (not self.wriEnab)
        self.wriAccel.set (self.wriSpeed / -sp.world.period, self.wriBrake, self.wriTorq / self.wriInert)
        self.wriSpeed.set (self.wriSpeed + self.wriAccel * sp.world.period)
        self.wriAng.set (self.wriAng + self.wriSpeed * sp.world.period)
        
        self.part ('hand and fingers')
        self.hanAng.set (self.hanAngSet, self.hanEnab)
        self.finAng.set (self.finAngSet, self.finEnab)
        
