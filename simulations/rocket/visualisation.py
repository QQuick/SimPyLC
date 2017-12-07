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

from SimPyLC import *

class Visualisation (Scene):
    def __init__ (self):
        Scene.__init__ (self)
        self.nose = Cone (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.body = Cylinder (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.bracket = Cylinder (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.gimbal = Sphere (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.thruster = Cone (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.flame = Cone (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        
    def display (self):
        self.body (parts = lambda:
            self.nose () +
            self.bracket (parts = lambda:
                self.thruster (parts = lambda:
                    self.flame ()
        )   )   )
        