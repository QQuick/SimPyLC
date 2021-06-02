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

class BlinkingLight (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        
        self.blinkTimer = sp.Timer ()
        self.pulse = sp.Oneshot ()
        self.counter = sp.Register ()
        self.led = sp.Marker ()
        self.run = sp.Runner ()
    
    def sweep (self):
        self.blinkTimer.reset (self.blinkTimer > 8)
        self.pulse.trigger (self.blinkTimer > 3)
        self.counter.set (self.counter + 1, self.pulse)
        self.led.mark (not self.led, self.pulse)
        
