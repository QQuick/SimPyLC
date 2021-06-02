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

class TrafficLamp (sp.Cylinder):
    def __init__ (self, green = False):
        sp.Cylinder.__init__ (self, size = (0.1, 0.1, 0.2), center = (0, 0, 0.5) if green else (0, 0, 0.7), color = (0, 1, 0) if green else (1, 0, 0))
        self.originalColor = self.color

    def __call__ (self, on):
        self.color = self.originalColor if on else sp.tsMul (self.originalColor, 0.2)
        return sp.Cylinder.__call__ (self)

class StreetLamp (sp.Cylinder):
    def __init__ (self, green = False):
        sp.Cylinder.__init__ (self, size = (0.4, 0.4, 0.4), center = (0, 0, 2), color = (1, 1, 0.2))
        self.originalColor = self.color

    def __call__ (self, brightness):
        self.color = sp.tsMul (self.originalColor, 0.2 + 0.8 * brightness)
        return sp.Cylinder.__call__ (self)

class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        
        self.crossing = sp.Beam (size = (3, 3, 0.1), pivot = (0, 1, 0), color = (0.1, 0.1, 0.1))
        self.sidewalk = sp.Beam (size = (1, 1, 0.1), center = (-1, -1, 0.1), joint = (1, 1, 0), color = (0, 0.3, 0)) 
        self.pole = sp.Cylinder (size = (0.05, 0.05, 1), center = (0, 0.45, 0.45), color = (1, 1, 1))
        
        self.redLamp = TrafficLamp ()
        self.greenLamp = TrafficLamp (True)
        self.streetLamp = StreetLamp ()     
        
    def display (self):
        control = sp.world.trafficLights
        
        self.crossing (rotation = 30, parts = lambda:
            self.sidewalk (rotation = 0, parts = lambda:
                self.pole (parts = lambda:
                    self.redLamp (control.northRedLamp) +
                    self.greenLamp (control.northGreenLamp)
                )
            ) +
            self.sidewalk (rotation = -90, parts = lambda:
                self.pole (parts = lambda:
                    self.redLamp (control.eastRedLamp) +
                    self.greenLamp (control.eastGreenLamp)
                )
        
            ) +
            self.sidewalk (rotation = -180, parts = lambda:
                self.pole (parts = lambda:
                    self.redLamp (control.southRedLamp) +
                    self.greenLamp (control.southGreenLamp)
                )
            ) +
            self.sidewalk (rotation = -270, parts = lambda:
                self.pole (parts = lambda:
                    self.redLamp (control.westRedLamp) +
                    self.greenLamp (control.westGreenLamp)
                )
            ) +
            self.streetLamp ((control.streetLamp - control.brightMin) / (control.brightMax - control.brightMin))
        )
    
