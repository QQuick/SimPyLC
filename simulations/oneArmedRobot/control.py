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

class Control (Module):
    def __init__ (self):
        Module.__init__ (self)
        
        self.page ('movement control')
        
        self.group ('torso drive control', True)
        self.torVoltFac = Register (0.8)
        self.torVoltMax = Register (10)
        self.torVolt = Register ()
        self.torEnab = Marker ()
        
        self.group ('torso angle')
        self.torAngSet = Register ()
        self.torAng = Register ()
        self.torAngOld = Register ()
        self.torAngDif = Register ()
        self.torMarg = Register (15)
        self.torRound = Marker ()
        self.torSpeedFac = Register (0.5)
        self.torSpeedMax = Register (20)
        self.torSpeedSet = Register()
        self.torSpeed = Register ()
        self.torSpeedDif = Register ()

        self.group ('general')
        self.go = Marker ()
        
        self.group ('upper arm drive control', True)
        self.uppVoltFac = Register (0.25)
        self.uppVoltMax = Register (10)
        self.uppVolt = Register ()
        self.uppEnab = Marker ()
        
        self.group ('upper arm angle')
        self.uppAngSet = Register ()
        self.uppAng = Register ()
        self.uppAngOld = Register ()
        self.uppAngDif = Register ()
        self.uppMarg = Register (15)
        self.uppRound = Marker ()
        self.uppSpeedFac = Register (0.5)
        self.uppSpeedMax = Register (20)
        self.uppSpeedSet = Register ()
        self.uppSpeed = Register ()
        self.uppSpeedDif = Register ()

        self.group ('fore arm drive control', True)
        self.forVoltFac = Register (0.25)
        self.forVoltMax = Register (10)
        self.forVolt = Register ()
        self.forEnab = Marker ()
        
        self.group ('fore arm angle')
        self.forAngSet = Register ()
        self.forAng = Register ()
        self.forAngOld = Register ()
        self.forAngDif = Register ()
        self.forMarg = Register (15)
        self.forRound = Marker ()
        self.forSpeedFac = Register (0.5)
        self.forSpeedMax = Register (20)
        self.forSpeedSet = Register ()
        self.forSpeed = Register ()
        self.forSpeedDif = Register ()
        
        self.group ('wrist drive control', True)
        self.wriVoltFac = Register (0.25)
        self.wriVoltMax = Register (10)
        self.wriVolt = Register ()
        self.wriEnab = Marker ()
        
        self.group ('wrist angle')
        self.wriAngSet = Register ()
        self.wriAng = Register ()
        self.wriAngOld = Register ()
        self.wriAngDif = Register ()
        self.wriMarg = Register (3)
        self.wriRound = Marker ()
        self.wriSpeedFac = Register (0.5)
        self.wriSpeedMax = Register (20)
        self.wriSpeedSet = Register ()
        self.wriSpeed = Register ()
        self.wriSpeedDif = Register ()
        
        self.group ('hand and fingers setpoints', True)
        self.hanAngSet = Register ()
        self.hanEnab = Marker ()
        self.finAngSet = Register ()
        self.finEnab = Marker ()
        self.finDelay = Register (1)
        self.finTimer = Timer ()
        self.finLatch = Latch ()
                
        self.group ('sweep time measurement')
        self.sweepMin = Register (1000)
        self.sweepMax = Register ()
        self.sweepWatch = Timer ()
        self.run = Runner ()
        
    def input (self):
        self.part ('true angles')
        self.torAng.set (world.robot.torAng)
        self.uppAng.set (world.robot.uppAng)
        self.forAng.set (world.robot.forAng)
        self.wriAng.set (world.robot.wriAng)
            
    def sweep (self):
        self.part ('torso')
        self.torAngDif.set (self.torAngSet - self.torAng)
        self.torRound.mark (abs (self.torAngDif) < self.torMarg)
        self.torSpeedSet.set (limit (self.torSpeedFac * self.torAngDif, self.torSpeedMax))
        self.torSpeed.set ((self.torAng - self.torAngOld) / world.period)
        self.torSpeedDif.set (self.torSpeedSet - self.torSpeed)
        self.torVolt.set (limit (self.torVoltFac * self.torSpeedDif, self.torVoltMax))
        self.torEnab.mark (self.go)
        self.torAngOld.set (self.torAng)
        
        self.part ('upper arm')
        self.uppAngDif.set (self.uppAngSet - self.uppAng)
        self.uppRound.mark (abs (self.uppAngDif) < self.uppMarg)
        self.uppSpeedSet.set (limit (self.uppSpeedFac * self.uppAngDif, self.uppSpeedMax))
        self.uppSpeed.set ((self.uppAng - self.uppAngOld) / world.period)
        self.uppSpeedDif.set (self.uppSpeedSet - self.uppSpeed)
        self.uppVolt.set (limit (self.uppVoltFac * self.uppSpeedDif, self.uppVoltMax))
        self.uppEnab.mark (self.go and self.torRound)
        self.uppAngOld.set (self.uppAng)
        
        self.part ('fore arm')
        self.forAngDif.set (self.forAngSet - self.forAng)
        self.forRound.mark (abs (self.forAngDif) < self.forMarg)
        self.forSpeedSet.set (limit (self.forSpeedFac * self.forAngDif, self.forSpeedMax))
        self.forSpeed.set ((self.forAng - self.forAngOld) / world.period)
        self.forSpeedDif.set (self.forSpeedSet - self.forSpeed)     
        self.forVolt.set (limit (self.forVoltFac * self.forSpeedDif, self.forVoltMax))
        self.forEnab.mark (self.go and self.torRound and self.uppRound)
        self.forAngOld.set (self.forAng)
        
        self.part ('wrist')
        self.wriAngDif.set (self.wriAngSet - self.wriAng)
        self.wriRound.mark (abs (self.wriAngDif) < self.wriMarg)
        self.wriSpeedSet.set (limit (self.wriSpeedFac * self.wriAngDif, self.wriSpeedMax))
        self.wriSpeed.set ((self.wriAng - self.wriAngOld) / world.period)
        self.wriSpeedDif.set (self.wriSpeedSet - self.wriSpeed)     
        self.wriVolt.set (limit (self.wriVoltFac * self.wriSpeedDif, self.wriVoltMax))
        self.wriEnab.mark (self.go and self.torRound and self.uppRound and self.forRound)
        self.wriAngOld.set (self.wriAng)
        
        self.part ('hand and fingers')
        self.hanEnab.mark (self.go and self.torRound and self.uppRound and self.forRound and self.wriRound)
        self.finTimer.reset (not self.hanEnab)
        self.finEnab.mark (self.finTimer > self.finDelay)
        self.finLatch.latch (self.finTimer > 0.01)
        
        self.part ('sweep time measurement')
        self.sweepMin.set (world.period, world.period < self.sweepMin)
        self.sweepMax.set (world.period, world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        self.sweepMax.set (0, not self.sweepWatch)
        