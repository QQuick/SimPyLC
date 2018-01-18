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

class Control (Module):
    def __init__ (self):
        Module.__init__ (self)
        
        self.page ('Four plate stove control with cooking alarm')
        
        self.group ('General buttons', True)
        self.powerButton = Marker ()
        self.powerEdge = Oneshot ()
        self.power = Marker ()
        
        self.group ()
        self.childLockButton = Marker ()
        self.childLockChangeTimer = Timer ()
        self.childLockEdge = Oneshot ()
        self.childLock = Marker ()
        self.unlocked = Marker ()
        
        self.group ('Plate selection')
        self.plateSelectButton = Marker ()
        self.plateSelectEdge = Oneshot ()
        self.plateSelectDelta = Register ()
        self.plateSelectNr = Register ()
        self.tempDelta = Register ()
        self.tempChange = Marker ()
        
        self.group ('Up/down buttons')
        self.upButton = Marker ()
        self.upEdge = Oneshot ()
        self.group ()
        self.downButton = Marker ()
        self.downEdge = Oneshot ()
        
        self.group ('Cooking plates', True)
        self.plate0Temp = Register ()
        self.plate0Selected = Marker ()
        
        self.group ()
        self.plate1Temp = Register ()
        self.plate1Selected = Marker ()
        
        self.group ()
        self.plate2Temp = Register ()
        self.plate2Selected = Marker ()
        
        self.group ()
        self.plate3Temp = Register ()
        self.plate3Selected = Marker ()
        
        self.group ('Alarm selection button')
        self.alarmSelectButton = Marker ()
        self.alarmSelectEdge = Oneshot ()
        self.alarmSelected = Marker ()
        self.alarmTime = Register ()
        self.alarmTimer = Timer ()
        self.alarmOn = Latch ()
        self.alarmEdge = Oneshot ()
        self.alarmTimeLeft = Register ()
        self.alarmChangeTimer = Timer ()
        self.alarmChangeStep = Register ()
        self.alarmDelta = Register ()
        
        self.group ('Numerical displays', True)
        self.digitIndex = Register ()
        self.plateDigitValue = Register ()
        self.alarmDigitValue = Register ()
        self.digitValue = Register ()
        self.digitDot = Marker ()
                
        self.group ('Buzzer')
        self.buzzerOnTime = Register (6)
        self.buzzerOnTimer = Timer ()
        self.buzzerOn = Latch ()
        self.buzzerBaseFreq = Register (300.)
        self.buzzerPitchTimer = Timer ()
        self.buzzerFreq = Register ()
        self.buzzerWaveTimer = Timer ()
        self.buzzerEdge = Oneshot ()
        self.buzzer = Marker ()
                
        self.group ('System')
        self.sweepMin = Register (1000)
        self.sweepMax = Register ()
        self.sweepWatch = Timer ()
        self.run = Runner ()
            
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
        self.alarmTime.set (0, self.power and self.upButton and self.downButton, limit (self.alarmTime + self.alarmDelta * world.period, 0, 9999))
        
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
        
        self.plate0Temp.set (limit (self.plate0Temp + self.tempDelta, 0, 9), self.tempChange and self.plate0Selected)
        self.plate1Temp.set (limit (self.plate1Temp + self.tempDelta, 0, 9), self.tempChange and self.plate1Selected)
        self.plate2Temp.set (limit (self.plate2Temp + self.tempDelta, 0, 9), self.tempChange and self.plate2Selected)
        self.plate3Temp.set (limit (self.plate3Temp + self.tempDelta, 0, 9), self.tempChange and self.plate3Selected)
        
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
        
        self.alarmDigitValue.set (digit (self.alarmTimeLeft, self.digitIndex))
        self.digitValue.set (self.alarmDigitValue, self.alarmSelected, self.plateDigitValue)
        
        self.digitDot.mark (self.plate0Selected, self.digitIndex == 3)
        self.digitDot.mark (self.plate1Selected, self.digitIndex == 2)
        self.digitDot.mark (self.plate2Selected, self.digitIndex == 1)
        self.digitDot.mark (self.plate3Selected, self.digitIndex == 0)
        self.digitDot.mark (True, self.childLock)
        self.digitDot.mark (False, self.alarmSelected)
        
        self.part ('Sweep time measurement')
        self.sweepMin.set (world.period, world.period < self.sweepMin)
        self.sweepMax.set (world.period, world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        self.sweepMax.set (0, not self.sweepWatch)
