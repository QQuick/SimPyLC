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

useQuaternions = True
useGramSchmidt = True   # Only matters if useQuaternions == False

g = 10

earthMoonDist = 500

earthDiam = 50
earthMass = 8e7

moonDiam = 15
moonMass = 1e6

# Gravity made proportional to r^-0.5 instead of r^-2 to get a more "telling" simulation

gamma = g * (earthDiam / 2) * (earthDiam / 2) / earthMass

def getGravVec (mass0, mass1, diam, relPos):
    relPos = sp.tEva (relPos)
    dist = sp.tNor (relPos)
    factor = -1 if dist > diam / 2 else 0.1
    return sp.tsMul (sp.tUni (relPos), factor * gamma * mass0 * mass1 / (dist * dist))
    



