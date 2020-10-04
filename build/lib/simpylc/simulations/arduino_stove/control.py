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

class Control (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        
        self.page ('Four plate stove control with cooking alarm')
        
        self.group ('General buttons', True)
        self.powerButton = sp.Marker ()
        self.powerEdge = sp.Oneshot ()
        self.power = sp.Marker ()
        
        self.group ()
        self.childLockButton = sp.Marker ()
        self.childLockChangeTimer = sp.Timer ()
        self.childLockEdge = sp.Oneshot ()
        self.childLock = sp.Marker ()
        self.unlocked = sp.Marker ()
        
        self.group ('Plate selection')
        self.plateSelectButton = sp.Marker ()
        self.plateSelectEdge = sp.Oneshot ()
        self.plateSelectDelta = sp.Register ()
        self.plateSelectNr = sp.Register ()
        self.tempDelta = sp.Register ()
        self.tempChange = sp.Marker ()
        
        self.group ('Up/down buttons')
        self.upButton = sp.Marker ()
        self.upEdge = sp.Oneshot ()
        self.group ()
        self.downButton = sp.Marker ()
        self.downEdge = sp.Oneshot ()
        
        self.group ('Cooking plates', True)
        self.plate0Temp = sp.Register ()
        self.plate0Selected = sp.Marker ()
        
        self.group ()
        self.plate1Temp = sp.Register ()
        self.plate1Selected = sp.Marker ()
        
        self.group ()
        self.plate2Temp = sp.Register ()
        self.plate2Selected = sp.Marker ()
        
        self.group ()
        self.plate3Temp = sp.Register ()
        self.plate3Selected = sp.Marker ()
        
        self.group ('Alarm selection button')
        self.alarmSelectButton = sp.Marker ()
        self.alarmSelectEdge = sp.Oneshot ()
        self.alarmSelected = sp.Marker ()
        self.alarmTime = sp.Register ()
        self.alarmTimer = sp.Timer ()
        self.alarmOn = sp.Latch ()
        self.alarmEdge = sp.Oneshot ()
        self.alarmTimeLeft = sp.Register ()
        self.alarmChangeTimer = sp.Timer ()
        self.alarmChangeStep = sp.Register ()
        self.alarmDelta = sp.Register ()
        
        self.group ('Numerical displays', True)
        self.digitIndex = sp.Register ()
        self.plateDigitValue = sp.Register ()
        self.alarmDigitValue = sp.Register ()
        self.digitValue = sp.Register ()
        self.digitDot = sp.Marker ()
                
        self.group ('Buzzer')
        self.buzzerOnTime = sp.Register (6)
        self.buzzerOnTimer = sp.Timer ()
        self.buzzerOn = sp.Latch ()
        self.buzzerBaseFreq = sp.Register (300.)
        self.buzzerPitchTimer = sp.Timer ()
        self.buzzerFreq = sp.Register ()
        self.buzzerWaveTimer = sp.Timer ()
        self.buzzerEdge = sp.Oneshot ()
        self.buzzer = sp.Marker ()
                
        self.group ('System')
        self.sweepMin = sp.Register (1000)
        self.sweepMax = sp.Register ()
        self.sweepWatch = sp.Timer ()
        self.run = sp.Runner ()
            
    def sweep (self):
        self.part ('Edge triggering of buttons')
        self.powerEdge.trigger (self.powerButton)
        self.power.mark (not self.power, not self.childLock and self.powerEdge)
        
        self.childLockChangeTimer.reset (not (self.power and self.childLockButton))
        self.childLockEdge.trigger (self.childLockChangeTimer > 5)
        self.childLock.mark (not self.childLock, self.childLockEdge)
        self.unlocked.mark (self.power and not self.childLock)
        
        self.plateSelectEdge.trigger (self.plateSelectButton)
        self.plateSelectDelta.set (1, self.unlocked and self.plateSelectEdge, 0)
        self.plateSelectNr.set ((self.plateSelectNr + self.plateSelectDelta) % 4, self.power, 0)

        self.upEdge.trigger (self.upButton)
        self.downEdge.trigger (self.downButton)
                
        self.part ('Cooking alarm')
        self.alarmSelectEdge.trigger (self.power and self.alarmSelectButton)
        self.alarmSelected.mark (not self.alarmSelected, self.unlocked and self.alarmSelectEdge)
        
        self.alarmChangeTimer.reset (not (self.alarmSelected and (self.upButton or self.downButton)))
        self.alarmChangeStep.set (1, self.alarmChangeTimer > 0, 0)
        self.alarmChangeStep.set (10, self.alarmChangeTimer > 10)  
        self.alarmChangeStep.set (100, self.alarmChangeTimer > 20)
        
        self.alarmDelta.set (-self.alarmChangeStep, self.downButton, self.alarmChangeStep)
        self.alarmTime.set (0, self.power and self.upButton and self.downButton, sp.limit (self.alarmTime + self.alarmDelta * sp.world.period, 0, 9999))
        
        self.alarmOn.latch (self.alarmChangeTimer > 0)
        self.alarmTimer.reset (not self.alarmOn or self.alarmChangeTimer > 0)
        self.alarmEdge.trigger (
            self.alarmTimer > self.alarmTime
            or
            (self.childLock and (self.powerButton or self.plateSelectButton or self.alarmSelectButton or self.plateSelectButton or self.upButton or self.downButton))
        )
        self.alarmOn.unlatch (self.alarmEdge or self.alarmTime == 0)
    
        self.alarmTimeLeft.set (max ((self.alarmTime - self.alarmTimer), 0))
        
        self.part ('Cooking plates')
        self.plate0Selected.mark (self.plateSelectNr == 0)
        self.plate1Selected.mark (self.plateSelectNr == 1)
        self.plate2Selected.mark (self.plateSelectNr == 2)
        self.plate3Selected.mark (self.plateSelectNr == 3)
        
        self.tempChange.mark (self.unlocked and not self.alarmSelected and (self.upEdge or self.downEdge))
        self.tempDelta.set (-1, not self.alarmSelected and self.downButton, 1)
        
        self.plate0Temp.set (sp.limit (self.plate0Temp + self.tempDelta, 0, 9), self.tempChange and self.plate0Selected)
        self.plate1Temp.set (sp.limit (self.plate1Temp + self.tempDelta, 0, 9), self.tempChange and self.plate1Selected)
        self.plate2Temp.set (sp.limit (self.plate2Temp + self.tempDelta, 0, 9), self.tempChange and self.plate2Selected)
        self.plate3Temp.set (sp.limit (self.plate3Temp + self.tempDelta, 0, 9), self.tempChange and self.plate3Selected)
        
        self.part ('Buzzer tone generation and pitch bend')
        self.buzzerOn.latch (self.alarmEdge)
        self.buzzerOnTimer.reset (not self.buzzerOn)
        self.buzzerOn.unlatch (self.buzzerOnTimer > self.buzzerOnTime)
        
        self.buzzerPitchTimer.reset (self.buzzerPitchTimer > 3)
        self.buzzerFreq.set (self.buzzerBaseFreq * (1 + self.buzzerPitchTimer))
        self.buzzerWaveTimer.reset (self.buzzerWaveTimer > 0.5 / self.buzzerFreq)
        self.buzzerEdge.trigger (self.buzzerWaveTimer == 0)
        self.buzzer.mark (not self.buzzer, self.buzzerOn and self.buzzerEdge)
        
        self.part ('Numerical display')
        self.digitIndex.set ((self.digitIndex + 1) % 4)

        self.plateDigitValue.set (self.plate0Temp, self.digitIndex == 3)
        self.plateDigitValue.set (self.plate1Temp, self.digitIndex == 2)
        self.plateDigitValue.set (self.plate2Temp, self.digitIndex == 1)
        self.plateDigitValue.set (self.plate3Temp, self.digitIndex == 0)
        
        self.alarmDigitValue.set (sp.digit (self.alarmTimeLeft, self.digitIndex))
        self.digitValue.set (self.alarmDigitValue, self.alarmSelected, self.plateDigitValue)
        
        self.digitDot.mark (self.plate0Selected, self.digitIndex == 3)
        self.digitDot.mark (self.plate1Selected, self.digitIndex == 2)
        self.digitDot.mark (self.plate2Selected, self.digitIndex == 1)
        self.digitDot.mark (self.plate3Selected, self.digitIndex == 0)
        self.digitDot.mark (True, self.childLock)
        self.digitDot.mark (False, self.alarmSelected)
        
        self.part ('Sweep time measurement')
        self.sweepMin.set (sp.world.period, sp.world.period < self.sweepMin)
        self.sweepMax.set (sp.world.period, sp.world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        self.sweepMax.set (0, not self.sweepWatch)
