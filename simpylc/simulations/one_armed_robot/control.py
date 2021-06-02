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

class Control (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        
        self.page ('movement control')
        
        self.group ('torso drive control', True)
        self.torVoltFac = sp.Register (0.8)
        self.torVoltMax = sp.Register (10)
        self.torVolt = sp.Register ()
        self.torEnab = sp.Marker ()
        
        self.group ('torso angle')
        self.torAngSet = sp.Register ()
        self.torAng = sp.Register ()
        self.torAngOld = sp.Register ()
        self.torAngDif = sp.Register ()
        self.torMarg = sp.Register (15)
        self.torRound = sp.Marker ()
        self.torSpeedFac = sp.Register (0.5)
        self.torSpeedMax = sp.Register (20)
        self.torSpeedSet = sp.Register()
        self.torSpeed = sp.Register ()
        self.torSpeedDif = sp.Register ()

        self.group ('general')
        self.go = sp.Marker ()
        
        self.group ('upper arm drive control', True)
        self.uppVoltFac = sp.Register (0.25)
        self.uppVoltMax = sp.Register (10)
        self.uppVolt = sp.Register ()
        self.uppEnab = sp.Marker ()
        
        self.group ('upper arm angle')
        self.uppAngSet = sp.Register ()
        self.uppAng = sp.Register ()
        self.uppAngOld = sp.Register ()
        self.uppAngDif = sp.Register ()
        self.uppMarg = sp.Register (15)
        self.uppRound = sp.Marker ()
        self.uppSpeedFac = sp.Register (0.5)
        self.uppSpeedMax = sp.Register (20)
        self.uppSpeedSet = sp.Register ()
        self.uppSpeed = sp.Register ()
        self.uppSpeedDif = sp.Register ()

        self.group ('fore arm drive control', True)
        self.forVoltFac = sp.Register (0.25)
        self.forVoltMax = sp.Register (10)
        self.forVolt = sp.Register ()
        self.forEnab = sp.Marker ()
        
        self.group ('fore arm angle')
        self.forAngSet = sp.Register ()
        self.forAng = sp.Register ()
        self.forAngOld = sp.Register ()
        self.forAngDif = sp.Register ()
        self.forMarg = sp.Register (15)
        self.forRound = sp.Marker ()
        self.forSpeedFac = sp.Register (0.5)
        self.forSpeedMax = sp.Register (20)
        self.forSpeedSet = sp.Register ()
        self.forSpeed = sp.Register ()
        self.forSpeedDif = sp.Register ()
        
        self.group ('wrist drive control', True)
        self.wriVoltFac = sp.Register (0.25)
        self.wriVoltMax = sp.Register (10)
        self.wriVolt = sp.Register ()
        self.wriEnab = sp.Marker ()
        
        self.group ('wrist angle')
        self.wriAngSet = sp.Register ()
        self.wriAng = sp.Register ()
        self.wriAngOld = sp.Register ()
        self.wriAngDif = sp.Register ()
        self.wriMarg = sp.Register (3)
        self.wriRound = sp.Marker ()
        self.wriSpeedFac = sp.Register (0.5)
        self.wriSpeedMax = sp.Register (20)
        self.wriSpeedSet = sp.Register ()
        self.wriSpeed = sp.Register ()
        self.wriSpeedDif = sp.Register ()
        
        self.group ('hand and fingers setpoints', True)
        self.hanAngSet = sp.Register ()
        self.hanEnab = sp.Marker ()
        self.finAngSet = sp.Register ()
        self.finEnab = sp.Marker ()
        self.finDelay = sp.Register (1)
        self.finTimer = sp.Timer ()
        self.finLatch = sp.Latch ()
                
        self.group ('sweep time measurement')
        self.sweepMin = sp.Register (1000)
        self.sweepMax = sp.Register ()
        self.sweepWatch = sp.Timer ()
        self.run = sp.Runner ()
        
    def input (self):
        self.part ('true angles')
        self.torAng.set (sp.world.robot.torAng)
        self.uppAng.set (sp.world.robot.uppAng)
        self.forAng.set (sp.world.robot.forAng)
        self.wriAng.set (sp.world.robot.wriAng)
            
    def sweep (self):
        self.part ('torso')
        self.torAngDif.set (self.torAngSet - self.torAng)
        self.torRound.mark (sp.abs (self.torAngDif) < self.torMarg)
        self.torSpeedSet.set (sp.limit (self.torSpeedFac * self.torAngDif, self.torSpeedMax))
        self.torSpeed.set ((self.torAng - self.torAngOld) / sp.world.period)
        self.torSpeedDif.set (self.torSpeedSet - self.torSpeed)
        self.torVolt.set (sp.limit (self.torVoltFac * self.torSpeedDif, self.torVoltMax))
        self.torEnab.mark (self.go)
        self.torAngOld.set (self.torAng)
        
        self.part ('upper arm')
        self.uppAngDif.set (self.uppAngSet - self.uppAng)
        self.uppRound.mark (sp.abs (self.uppAngDif) < self.uppMarg)
        self.uppSpeedSet.set (sp.limit (self.uppSpeedFac * self.uppAngDif, self.uppSpeedMax))
        self.uppSpeed.set ((self.uppAng - self.uppAngOld) / sp.world.period)
        self.uppSpeedDif.set (self.uppSpeedSet - self.uppSpeed)
        self.uppVolt.set (sp.limit (self.uppVoltFac * self.uppSpeedDif, self.uppVoltMax))
        self.uppEnab.mark (self.go and self.torRound)
        self.uppAngOld.set (self.uppAng)
        
        self.part ('fore arm')
        self.forAngDif.set (self.forAngSet - self.forAng)
        self.forRound.mark (sp.abs (self.forAngDif) < self.forMarg)
        self.forSpeedSet.set (sp.limit (self.forSpeedFac * self.forAngDif, self.forSpeedMax))
        self.forSpeed.set ((self.forAng - self.forAngOld) / sp.world.period)
        self.forSpeedDif.set (self.forSpeedSet - self.forSpeed)     
        self.forVolt.set (sp.limit (self.forVoltFac * self.forSpeedDif, self.forVoltMax))
        self.forEnab.mark (self.go and self.torRound and self.uppRound)
        self.forAngOld.set (self.forAng)
        
        self.part ('wrist')
        self.wriAngDif.set (self.wriAngSet - self.wriAng)
        self.wriRound.mark (sp.abs (self.wriAngDif) < self.wriMarg)
        self.wriSpeedSet.set (sp.limit (self.wriSpeedFac * self.wriAngDif, self.wriSpeedMax))
        self.wriSpeed.set ((self.wriAng - self.wriAngOld) / sp.world.period)
        self.wriSpeedDif.set (self.wriSpeedSet - self.wriSpeed)     
        self.wriVolt.set (sp.limit (self.wriVoltFac * self.wriSpeedDif, self.wriVoltMax))
        self.wriEnab.mark (self.go and self.torRound and self.uppRound and self.forRound)
        self.wriAngOld.set (self.wriAng)
        
        self.part ('hand and fingers')
        self.hanEnab.mark (self.go and self.torRound and self.uppRound and self.forRound and self.wriRound)
        self.finTimer.reset (not self.hanEnab)
        self.finEnab.mark (self.finTimer > self.finDelay)
        self.finLatch.latch (self.finTimer > 0.01)
        
        self.part ('sweep time measurement')
        self.sweepMin.set (sp.world.period, sp.world.period < self.sweepMin)
        self.sweepMax.set (sp.world.period, sp.world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        self.sweepMax.set (0, not self.sweepWatch)
        
