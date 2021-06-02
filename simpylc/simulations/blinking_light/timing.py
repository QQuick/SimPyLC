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

class Timing (sp.Chart):
    def __init__ (self):
        sp.Chart.__init__ (self)
        
    def define (self):
        self.channel (sp.world.blinkingLight.blinkTimer, sp.red, 0, 12, 50)
        self.channel (sp.world.blinkingLight.pulse, sp.blue, 0, 1, 50)
        self.channel (sp.world.blinkingLight.counter, sp.yellow, 0, 20, 100)
        self.channel (sp.world.blinkingLight.led, sp.lime, 0, 1, 50)
        
