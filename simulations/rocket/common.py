import math

from SimPyLC import *

g = 10

earthMoonDist = 500

earthDiam = 50
earthMass = 8e7

moonDiam = 15
moonMass = 1e6

# Gravite made proportional to r^-0.5 instead of r^-2 to get a more "telling" simulation

gamma = g * (earthDiam / 2) * (earthDiam / 2) / earthMass

def getGravVec (mass0, mass1, diam, relPos):
    relPos = tEva (relPos)
    dist = tNor (relPos)
    factor = -1 if dist > diam / 2 else 0.1
    return tsMul (tUni (relPos), factor * gamma * mass0 * mass1 / (dist * dist))
    



