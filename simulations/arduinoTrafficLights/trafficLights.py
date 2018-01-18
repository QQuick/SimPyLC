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

class TrafficLights (Module):
    def __init__ (self):
        Module.__init__ (self)  
        
        self.page ('Trafic lights')
        
        self.group ('Timers', True)
        self.regularPhaseTimer = Timer ()
        self.cyclePhaseTimer = Timer ()
        self.tBlink = Register (0.3)
        self.blinkTimer = Timer ()
        self.blinkPulse = Oneshot ()
        self.blink = Marker ()
                
        self.group ('Mode switching')
        self.modeButton = Marker ()
        self.modePulse = Oneshot ()
        self.modeStep = Register ()
        self.regularMode = Marker (True)
        self.cycleMode = Marker ()
        self.nightMode = Marker ()
        self.offMode = Marker ()
            
        self.group ('Night blinking')
        self.allowRed = Marker ()
        
        self.group ('Regular mode phases', True)
        self.northSouthGreen = Marker (True)
        self.northSouthBlink = Marker ()
        self.eastWestGreen = Marker ()
        self.eastWestBlink = Marker ()
        
        self.group ('Cycle mode phases')
        self.northGreen = Marker ()
        self.northBlink = Marker ()
        self.eastGreen = Marker ()
        self.eastBlink = Marker ()
        self.southGreen = Marker ()
        self.southBlink = Marker ()
        self.westGreen = Marker ()
        self.westBlink = Marker ()
        
        self.group ('Lamps')
        self.northGreenLamp = Marker ()
        self.northRedLamp = Marker ()
        self.eastGreenLamp = Marker ()
        self.eastRedLamp = Marker ()
        self.southGreenLamp = Marker ()
        self.southRedLamp = Marker ()
        self.westGreenLamp = Marker ()
        self.westRedLamp = Marker ()        
        
        self.group ('Regular phase end times', True)
        self.tNorthSouthGreen = Register (5)
        self.tNorthSouthBlink = Register (7)
        self.tEastWestGreen = Register (12)
        self.tEastWestBlink = Register (14)
        
        self.group ('Cycle phase end times')
        self.tNorthGreen = Register (5)
        self.tNorthBlink = Register (7)
        self.tEastGreen = Register (12)
        self.tEastBlink = Register (14)
        self.tSouthGreen = Register (19)
        self.tSouthBlink = Register (21)
        self.tWestGreen = Register (26)
        self.tWestBlink = Register (28)
        
        self.group ('Street illumination')
        self.brightButton = Marker ()
        self.brightPulse = Oneshot ()
        self.brightDirection = Marker (True)
        self.brightMin = Register (2047)
        self.brightMax = Register (4095)
        self.brightFluxus = Register (200)
        self.brightDelta = Register ()
        self.streetLamp = Register (2047)
        
        self.group ('System')
        self.runner = Runner ()
            
    def sweep (self):
        self.part ('Timers')
        self.regularPhaseTimer.reset (self.regularPhaseTimer > self.tEastWestBlink or self.cycleMode or self.nightMode or self.offMode)
        self.cyclePhaseTimer.reset (self.cyclePhaseTimer > self.tWestBlink or self.regularMode or self.nightMode or self.offMode)
        self.blinkTimer.reset (self.blinkTimer > self.tBlink)
        self.blinkPulse.trigger (self.blinkTimer == 0)
        self.blink.mark (not self.blink, self.blinkPulse)
        
        self.part ('Mode switching')
        self.modePulse.trigger (self.modeButton)
        self.modeStep.set ((self.modeStep + 1) % 4, self.modePulse)
        self.regularMode.mark (self.modeStep == 0)
        self.cycleMode.mark (self.modeStep == 1)
        self.nightMode.mark (self.modeStep == 2)
        self.offMode.mark (self.modeStep == 3)
        
        self.part ('Regular mode phases')
        self.northSouthGreen.mark (0 < self.regularPhaseTimer < self.tNorthSouthGreen)
        self.northSouthBlink.mark (self.tNorthSouthGreen < self.regularPhaseTimer < self.tNorthSouthBlink)
        self.eastWestGreen.mark (self.tNorthSouthBlink < self.regularPhaseTimer < self.tEastWestGreen)
        self.eastWestBlink.mark (self.tEastWestGreen < self.regularPhaseTimer)
        
        self.part ('Cycle mode phases')
        self.northGreen.mark (0 < self.cyclePhaseTimer < self.tNorthGreen)
        self.northBlink.mark (self.tNorthGreen < self.cyclePhaseTimer < self.tNorthBlink)
        self.eastGreen.mark (self.tNorthBlink < self.cyclePhaseTimer < self.tEastGreen)
        self.eastBlink.mark (self.tEastGreen < self.cyclePhaseTimer < self.tEastBlink)
        self.southGreen.mark (self.tEastBlink < self.cyclePhaseTimer < self.tSouthGreen)
        self.southBlink.mark (self.tSouthGreen < self.cyclePhaseTimer < self.tSouthBlink)
        self.westGreen.mark (self.tSouthBlink < self.cyclePhaseTimer < self.tWestGreen)
        self.westBlink.mark (self.tWestGreen < self.cyclePhaseTimer)
        
        self.part ('Night blinking')
        self.allowRed.mark (self.regularMode or self.cycleMode or (self.nightMode and self.blink))
        
        self.part ('Traffic lamps')
        self.northGreenLamp.mark (self.northSouthGreen or self.northGreen or ((self.northSouthBlink or self.northBlink) and self.blink))
        self.northRedLamp.mark (not (self.northSouthGreen or self.northGreen or self.northSouthBlink or self.northBlink) and self.allowRed)
        self.eastGreenLamp.mark (self.eastWestGreen or self.eastGreen or ((self.eastWestBlink or self.eastBlink) and self.blink))
        self.eastRedLamp.mark (not (self.eastWestGreen or self.eastGreen or self.eastWestBlink or self.eastBlink) and self.allowRed)
        self.southGreenLamp.mark (self.northSouthGreen or self.southGreen or ((self.northSouthBlink or self.southBlink) and self.blink))
        self.southRedLamp.mark (not (self.northSouthGreen or self.southGreen or self.northSouthBlink or self.southBlink) and self.allowRed)
        self.westGreenLamp.mark (self.eastWestGreen or self.westGreen or ((self.eastWestBlink or self.westBlink) and self.blink))
        self.westRedLamp.mark (not (self.eastWestGreen or self.westGreen or self.eastWestBlink or self.westBlink) and self.allowRed)
        
        self.part ('Street illumination')
        self.brightPulse.trigger (self.brightButton)
        self.brightDirection.mark (not self.brightDirection, self.brightPulse)
        self.brightDelta.set (-self.brightFluxus * world.period, self.brightDirection, self.brightFluxus * world.period)
        self.streetLamp.set (limit (self.streetLamp + self.brightDelta, self.brightMin, self.brightMax), self.brightButton)
        