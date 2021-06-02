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

class PidController (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)
        
        self.page ('p i d controller')

        self.group ('inputs', True)
        self.uRefIn = sp.Register ()
        self.uActIn = sp.Register ()

        self.group ('outputs')
        self.uOut = sp.Register ()

        self.group ('p i d settings')
        self.cProp = sp.Register ()
        self.cInt = sp.Register (1)
        self.cDif = sp.Register ()

        self.group ('raw correction terms', True)
        self.uCorIn = sp.Register ()
        self.uCorIntIn = sp.Register ()
        self.uCorDifIn = sp.Register ()

        self.group ('scaled correction terms')
        self.uCorOut = sp.Register ()
        self.uCorIntOut = sp.Register ()
        self.uCorDifOut = sp.Register ()

        self.group ('auxiliary', True)
        self.uMax = sp.Register (3.5)
        self.nMax = sp.Register (1024)
        self.uCorOldIn = sp.Register ()
        self.nActIn = sp.Register ()
        self.nOut = sp.Register ()

        self.group ('physics')
        self.simulatePhysics = sp.Marker ()
        self.transferFactor = sp.Register (1)
        
    def sweep (self):
        self.uRefIn.set (self.uMax / 2)
        self.nActIn.set (self.transferFactor * self.nOut, self.simulatePhysics)
        self.uActIn.set (self.nActIn * self.uMax / self.nMax)

        self.uCorOldIn.set (self.uCorIn)
        self.uCorIn.set (self.uRefIn - self.uActIn)
        self.uCorIntIn.set (sp.limit (self.uCorIntIn + self.uCorIn * sp.world.period, self.uMax))
        self.uCorDifIn.set ((self.uCorIn - self.uCorOldIn) / sp.world.period)

        self.uCorOut.set (self.cProp * self.uCorIn)
        self.uCorIntOut.set (self.cInt * self.uCorIntIn)
        self.uCorDifOut.set (self.cDif * self.uCorDifIn)

        self.uOut.set (self.uCorOut + self.uCorIntOut + self.uCorDifOut)
        self.nOut.set (self.uOut * self.nMax / self.uMax)