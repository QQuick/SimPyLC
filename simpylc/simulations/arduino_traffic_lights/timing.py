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
        self.channel (sp.world.trafficLights.northGreenLamp, sp.green)
        self.channel (sp.world.trafficLights.northRedLamp, sp.red)
        self.channel (sp.world.trafficLights.eastGreenLamp, sp.green)
        self.channel (sp.world.trafficLights.eastRedLamp, sp.red)
        self.channel (sp.world.trafficLights.southGreenLamp, sp.green)
        self.channel (sp.world.trafficLights.southRedLamp, sp.red)
        self.channel (sp.world.trafficLights.westGreenLamp, sp.green)
        self.channel (sp.world.trafficLights.westRedLamp, sp.red)
        self.channel (sp.world.trafficLights.regularPhaseTimer, sp.aqua, 0, 20, 60)
        self.channel (sp.world.trafficLights.cyclePhaseTimer, sp.aqua, 0, 40, 60)
        self.channel (sp.world.trafficLights.blinkTimer, sp.aqua, 0, 0.3, 60)
        self.channel (sp.world.trafficLights.modeButton, sp.white)
        self.channel (sp.world.trafficLights.modePulse, sp.white)
        self.channel (sp.world.trafficLights.modeStep, sp.white, 0, 3, 60)
        self.channel (sp.world.trafficLights.brightButton, sp.yellow)
        self.channel (sp.world.trafficLights.brightPulse, sp.yellow)
        self.channel (sp.world.trafficLights.brightDirection, sp.yellow)
        self.channel (sp.world.trafficLights.streetLamp, sp.yellow, 0, 5000, 60)
        
