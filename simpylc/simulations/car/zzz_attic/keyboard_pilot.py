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

import time as tm

import simpylc as sp

class KeyboardPilot:
    def __init__ (self):
        print ('Use arrow keys to control speed and direction')
        
        while True:
            self.input ()
            self.sweep ()
            self.output ()
            tm.sleep (0.02)
            
    def input (self):
        key = sp.getKey ()
        
        self.leftKey = key == 'KEY_LEFT'
        self.rightKey = key == 'KEY_RIGHT'
        self.upKey = key == 'KEY_UP'
        self.downKey = key == 'KEY_DOWN'

        self.targetVelocityStep = sp.world.control.targetVelocityStep
        self.steeringAngleStep = sp.world.control.steeringAngleStep

    def sweep (self):
        if self.leftKey:
            self.steeringAngleStep += 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.rightKey:
            self.steeringAngleStep -= 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.upKey:
            self.targetVelocityStep += 1
            print ('Target velocity step: ', self.targetVelocityStep)
        elif self.downKey:
            self.targetVelocityStep -= 1
            print ('Target velocity step: ', self.targetVelocityStep)
        
    def output (self):
        sp.world.control.steeringAngleStep.set (self.steeringAngleStep)
        sp.world.control.targetVelocityStep.set (self.targetVelocityStep)
        
