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

class Visualisation (Scene):
    def __init__ (self):
        Scene.__init__ (self)
        self.base = Cylinder (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.torso = Beam (size = (0.4, 0.4, 0.6), center = (0, 0, 0.5), pivot = (0, 0, 1), color = (0.5, 0.5, 0.5))
        
        armColor = (0.7, 0.7, 0.7)
        self.upperArm = Beam (size = (1, 0.2, 0.2), center = (0.4, -0.3, 0.1), joint = (-0.4, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.foreArm = Beam (size = (0.7, 0.15, 0.15), center = (0.65, 0.175, 0), joint = (-0.25, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.wrist = Beam (size = (0.3, 0.1, 0.1), center = (0.40, -0.125, 0), joint = (-0.05, 0, 0), pivot = (0, 1, 0), color = armColor)
        
        handColor = (1, 0.01, 0.01)
        handSideSize = (0.1, 0.1, 0.1)
        self.handCenter = Beam (size = (0.1, 0.09, 0.09), center = (0.15, 0, 0), pivot = (1, 0, 0), color = handColor)
        self.handSide0 = Beam (size = handSideSize, center = (0, -0.075, -0.075), color = handColor)
        self.handSide1 = Beam (size = handSideSize, center = (0, 0.075, -0.075), color = handColor)
        self.handSide2 = Beam (size = handSideSize, center = (0, 0.075, 0.075), color = handColor)
        self.handSide3 = Beam (size = handSideSize, center = (0, -0.075, 0.075), color = handColor)
        
        fingerColor = (0.01, 1, 0.01)
        fingerSize = (0.3, 0.05, 0.05)
        fingerJoint = (-0.125, 0, 0)
        self.finger0 = Beam (size = fingerSize, center = (0.15, 0, -0.1), joint = fingerJoint, pivot = (0, -1, 0), color = fingerColor)
        self.finger1 = Beam (size = fingerSize, center = (0.15, 0, 0.1), joint = fingerJoint, pivot = (0, 1, 0), color = fingerColor)
        self.finger2 = Beam (size = fingerSize, center = (0.15, -0.1, 0), joint = fingerJoint, pivot = (0, 0, 1), color = fingerColor)
        self.finger3 = Beam (size = fingerSize, center = (0.15, 0.1, 0), joint = fingerJoint, pivot = (0, 0, -1), color = fingerColor)
        
    def display (self):
        self.base (parts = lambda:
            self.torso (rotation = world.robot.torAng, parts = lambda:
                self.upperArm (rotation = world.robot.uppAng, parts = lambda:
                    self.foreArm (rotation = world.robot.forAng, shift = (world.robot.forShift, 0, 0), parts = lambda:
                        self.wrist (rotation = world.robot.wriAng, parts = lambda:
                            self.handCenter (rotation = world.robot.hanAng, parts = lambda:
                                self.handSide0 () +
                                self.handSide1 () +
                                self.handSide2 () +
                                self.handSide3 () +
                                self.finger0 (rotation = world.robot.finAng) +
                                self.finger1 (rotation = world.robot.finAng) +
                                self.finger2 (rotation = world.robot.finAng) +
                                self.finger3 (rotation = world.robot.finAng)
        )   )   )   )   )   )
        