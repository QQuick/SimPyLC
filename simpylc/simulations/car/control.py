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

import parameters as pm

class Control (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        
        self.page ('motion control')
        
        self.group ('driver input', True)
        self.targetVelocityStep = sp.Register (0)
        self.steeringAngleStep = sp.Register (2)

        self.group ('control output')
        self.targetVelocity = sp.Register ()
        self.steeringAngle = sp.Register ()
                
        self.group ('sweep time measurement', True)
        self.sweepMin = sp.Register (1000)
        self.sweepMax = sp.Register ()
        self.sweepWatch = sp.Timer ()
        self.run = sp.Runner ()
        
    def output (self):
        sp.world.physics.targetVelocity.set (self.targetVelocity)
        sp.world.physics.steeringAngle.set (self.steeringAngle)
        
    def sweep (self):
        # Input to output
        self.targetVelocity.set (0.2 * self.targetVelocityStep)
        self.steeringAngle.set (10 * self.steeringAngleStep)
        
        # Sweep time measurement
        self.sweepMin.set (sp.world.period, sp.world.period < self.sweepMin)
        self.sweepMax.set (sp.world.period, sp.world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        self.sweepMax.set (0, not self.sweepWatch)
        
