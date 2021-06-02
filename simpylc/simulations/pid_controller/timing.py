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

absRange = 5
absHeight = 75

class Timing (sp.Chart):
    def __init__ (self):
        sp.Chart.__init__ (self)
        
    def define (self):
        self.channel (sp.world.pidController.uRefIn, sp.lime, 0, absRange, absHeight)
        self.channel (sp.world.pidController.uActIn, sp.lime, 0, absRange, absHeight)
        
        self.channel (sp.world.pidController.uCorOut, sp.white, -absRange, absRange, 2 * absHeight)
        self.channel (sp.world.pidController.uCorIntOut, sp.white, -absRange, absRange, 2 * absHeight)
        self.channel (sp.world.pidController.uCorDifOut, sp.white, -absRange, absRange, 2 *absHeight)
        
        self.channel (sp.world.pidController.uOut, sp.lime, 0, absRange, absHeight)
