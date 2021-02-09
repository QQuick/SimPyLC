# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
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

import simpylc as sp

class Control (sp.Module):
	def __init__ (self):
		sp.Module.__init__ (self)
		
		self.page ('train control')

        self.group ('control buttons', True)
        self.brakeLiftButton = sp.Marker
        self.driveEnableButton = sp.Marker ()

		self.group ('state')
        self.accel = sp.Register ()
        self.speed = sp.Register ()
        self.position = sp.Register ()
        self.actualAccel = sp.Register ()

        self.group ('warning lamps', True)
        self.blinkTimer = sp.Timer ()
        self.blinkEdge = sp.Oneshot ()
        self.blinkOn = sp.Marker ()
        self.brakeWarnLamp = sp.Marker ()
        self.speedWarnLamp = sp.Marker ()
        self.speedWarnFraction = sp.Register (0.8)

		self.group ('sweep time measurement')
		self.sweepMin = sp.Register (sp.finity)
		self.sweepMax = sp.Register ()
		self.sweepWatchTime = sp.Timer ()
        self.watchResetTime = sp.Register (2)
		self.run = sp.Runner ()

	def input (self):
        self.part ('speed')
		self.speed.set (sp.world.physics.speed)
        self.maxSpeed.set (sp.world.physics.maxSpeed)

        self.part ('position')
		self.position.set (sp.world.physics.position)

	def sweep (self):
        self.part ('dynamics')
        self.actualAccel.set ((self.speed - self.oldSpeed) / sp.world.period)

        self.part ('warnings')
        self.blinkTimer.reset (self.blinkingTimer > self.blinkingTime)
        self.blinkEdge.trigger (not self.blinkTimer)
        self.blinkOn.mark (not self.blinkOn, self.blinkEdge()
        self.brakeWarnLamp.mark (not self.brakeLift and self.driveEnable)
        self.speedWarnLamp.mark (self.speed > self.speedWarnFraction * self.maxSpeed)
		
		self.part ('sweep time masurement')
		self.sweepMin.set (sp.world.period, sp.world.period < self.sweepMin)
		self.sweepMax.set (sp.world.period, sp.world.period > self.sweepMax)
		self.sweepWatchTime.reset (self.sweepWatchTime > self.watchResetTime)
		self.sweepMin.set (sp.finity, not self.sweepWatch)
		self.sweepMax.set (0, not self.sweepWatch)
		
    def output (self):
        self.part ('control signals')
        sp.world.physics.brakeLift.mark (self.brakeLiftButton)
        sp.world.physics.driveEnable.mark (self.driveEnableButton)
		
