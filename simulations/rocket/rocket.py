# ====== Legal notices
#
# Copyright (C) 2013 - 2018 GEATEC engineering
#
# This program is free software./
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

import numpy

from SimPyLC import *

from common import *

from transforms import *

# General remarks:
# - The physical reality of precession indicates that rotation matrix cannot be
#   found by applying angular acceleration in x, y and z direction successively.
# - To avoid gimbal lock, non-unique Euler angles and numerical instability of
#   (modified) Gram Schmidt, the use of quaternions seems the simplest way to go.

class Rocket (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.page ('rocket physics')
        
        self.group ('gimbal angle blue/yellow', True)
        self.blueYellowDelta = Register ()
        self.blueYellowRoughAngle = Register ()
        self.blueYellowAngle = Register ()
        
        self.group ('thruster angle green/red') 
        self.greenRedDelta = Register ()
        self.greenRedRoughAngle = Register ()
        self.greenRedAngle = Register ()
        
        self.group ('fuel throttle')
        self.throttleDelta = Register ()
        self.throttlePercent = Register ()
        self.thrust = Register ()      
        
        self.group ('ship')
        self.shipMass = Register (5000)
        self.effectiveRadius = Register (0.15)
        self.effectiveHeight = Register (1.5)
        self.thrusterTiltSpeed = Register (30)
        self.thrusterMaxAngle = Register (90)
        self.throttleSpeed = Register (20)
        self.thrusterMaxForce = Register (100000)
        
        self.group ('sweep time measurement')
        self.sweepMin = Register (1000)
        self.sweepMax = Register ()
        self.sweepWatch = Timer ()
        self.run = Runner ()        
        
        self.group ('linear accelleration', True)
        self.linAccelX = Register ()
        self.linAccelY = Register ()
        self.linAccelZ = Register ()
        
        self.group ('linear velocity')
        self.linVelocX = Register ()
        self.linVelocY = Register ()
        self.linVelocZ = Register ()
        
        self.group ('position')
        self.positionX = Register ()
        self.positionY = Register ()
        self.positionZ = Register (earthDiam / 2)
        
        self.group ('thrust in ship frame')
        self.forwardThrust = Register ()
        self.blueYellowThrust = Register ()
        self.greenRedThrust = Register ()
        
        self.group ('thrust in world frame')
        self.thrustX = Register ()
        self.thrustY = Register ()
        self.thrustZ = Register ()
        
        self.group ('angular acceleration', True)
        self.angAccelX = Register ()
        self.angAccelY = Register ()
        self.angAccelZ = Register ()
        
        self.group ('angular velocity')
        self.angVelocX = Register ()
        self.angVelocY = Register ()
        self.angVelocZ = Register ()
        
        self.group ('torques in ship frame')
        self.blueYellowTorque = Register ()
        self.greenRedTorque = Register ()
        
        self.group ('torques in world frame')
        self.torqueX = Register ()
        self.torqueY = Register ()
        self.torqueZ = Register ()
                
        if useQuaternions:
            self._shipRotQuat = quatFromAxAng (numpy.array ((1, 0, 0)), 0)
        
            self.group ('ship rotation quaternion')
            self.shipRotQuat0 = Register ()
            self.shipRotQuat1 = Register ()
            self.shipRotQuat2 = Register ()
            self.shipRotQuat3 = Register ()
            self._shipRotMat = rotMatFromQuat (self._shipRotQuat)
        else:
            self._shipRotMat = numpy.array ([   # Columns are tangent (front), normal (up) and binormal (starboard) of ship
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ])
                              
        self.group ('attitude')
        self.attitudeX = Register ()
        self.attitudeY = Register ()
        self.attitudeZ = Register ()
        
        self.group ('earth gravity', True)
        self.distEarthSurf = Register ()        
        self.earthGravX = Register ()
        self.earthGravY = Register ()
        self.earthGravZ = Register ()
        
        self.group ('moon gravity')
        self.distMoonSurf = Register ()
        self.moonGravX = Register ()
        self.moonGravY = Register ()
        self.moonGravZ = Register ()
        
        self.group ('total force')
        self.totalForceX = Register ()
        self.totalForceY = Register ()
        self.totalForceZ = Register ()
        
    def input (self):   
        self.part ('gimbal angle blue/yellow')
        self.blueYellowDelta.set (world.control.blueYellowDelta)
        
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (world.control.greenRedDelta)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (world.control.throttleDelta)
        
    def sweep (self):
        self.part ('gimbal angle blue/yellow')
        self.blueYellowRoughAngle.set (
            limit (
                self.blueYellowRoughAngle + self.blueYellowDelta * self.thrusterTiltSpeed * world.period,
                self.thrusterMaxAngle
            )
        )
        self.blueYellowAngle.set (snap (self.blueYellowRoughAngle, 0, 3))

        self.part ('thruster angle green/red')
        self.greenRedRoughAngle.set (
            limit (
                self.greenRedRoughAngle + self.greenRedDelta * self.thrusterTiltSpeed * world.period,
                self.thrusterMaxAngle
            )
        )
        self.greenRedAngle.set (snap (self.greenRedRoughAngle, 0, 3))
        
        self.part ('fuel throttle')
        self.throttlePercent.set (
            limit (
                self.throttlePercent + self.throttleDelta * self.throttleSpeed * world.period,
                0,
                100
            )
        )
        self.thrust.set (self.throttlePercent * self.thrusterMaxForce / 100)

        self.part ('linear movement')
        
        thrusterRotQuat = quatMul (
            quatFromAxAng (numpy.array ((1, 0, 0)), self.blueYellowAngle),
            quatFromAxAng (numpy.array ((0, 1, 0)), -self.greenRedAngle)
        )
        
        thrusterForceVec = numpy.array ((0, 0, self.thrust ()))
        shipForceVec = quatVecRot (thrusterRotQuat, thrusterForceVec)
        
        self.forwardThrust.set (shipForceVec [2])
        self.blueYellowThrust.set (shipForceVec [1])
        self.greenRedThrust.set (shipForceVec [0])
        
        if useQuaternions:
            worldForceVec = quatVecRot (self._shipRotQuat, shipForceVec)
        else:
            worldForceVec = self._shipRotMat @ shipForceVec 
            
        self.thrustX.set (worldForceVec [0])
        self.thrustY.set (worldForceVec [1])
        self.thrustZ.set (worldForceVec [2])
             
        earthGravVec = getGravVec (self.shipMass, earthMass, earthDiam, tEva ((self.positionX, self.positionY, self.positionZ)))
        self.earthGravX.set (earthGravVec [0])
        self.earthGravY.set (earthGravVec [1])
        self.earthGravZ.set (earthGravVec [2])  
      
        moonGravVec = getGravVec (self.shipMass, moonMass, moonDiam, tSub (tEva ((self.positionX, self.positionY, self.positionZ)), (0, 0, earthMoonDist)))
        self.moonGravX.set (moonGravVec [0])
        self.moonGravY.set (moonGravVec [1])
        self.moonGravZ.set (moonGravVec [2])
        
        self.totalForceX.set (self.thrustX + self.earthGravX + self.moonGravX)
        self.totalForceY.set (self.thrustY + self.earthGravY + self.moonGravY)
        self.totalForceZ.set (self.thrustZ + self.earthGravZ + self.moonGravZ)
        
        self.linAccelX.set (self.totalForceX / self.shipMass)
        self.linAccelY.set (self.totalForceY / self.shipMass)
        self.linAccelZ.set (self.totalForceZ / self.shipMass)
        
        self.linVelocX.set (self.linVelocX + self.linAccelX * world.period)
        self.linVelocY.set (self.linVelocY + self.linAccelY * world.period)
        self.linVelocZ.set (self.linVelocZ + self.linAccelZ * world.period)
        
        self.positionX.set (self.positionX + self.linVelocX * world.period)
        self.positionY.set (self.positionY + self.linVelocY * world.period)
        self.positionZ.set (self.positionZ + self.linVelocZ * world.period)
        
        self.part ('angular movement')
        
        rSq = self.effectiveRadius * self.effectiveRadius
        hSq = self.effectiveHeight * self.effectiveHeight

        # Source: https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors        
        shipInertMat = self.shipMass () / 12 * numpy.array  (
            (
                ((3 * rSq + hSq) / 12   , 0                     , 0      ),
                (0                      , (3 * rSq + hSq) / 12  , 0      ),
                (0                      , 0                     , rSq / 6)
            )
        )
        invInertMat = numpy.linalg.inv (self._shipRotMat @ shipInertMat @ self._shipRotMat.T)
                
        self.blueYellowTorque.set (self.blueYellowThrust * self.effectiveHeight / 2)
        self.greenRedTorque.set (-self.greenRedThrust * self.effectiveHeight / 2)
        shipTorqueVec = numpy.array ((self.blueYellowTorque (), self.greenRedTorque (), 0))
        
        if useQuaternions:
            rawTorqueVec = quatVecRot (self._shipRotQuat, shipTorqueVec)
        else:
            rawTorqueVec = self._shipRotMat @ shipTorqueVec
        self.torqueX.set (rawTorqueVec [0])
        self.torqueY.set (rawTorqueVec [1])
        self.torqueZ.set (rawTorqueVec [2])
        torqueVec = numpy.array ((self.torqueX (), self.torqueY (), self.torqueZ ()))
        
        rawAngAccelVec = degreesPerRadian * invInertMat @ torqueVec
        
        self.angAccelX.set (rawAngAccelVec [0])
        self.angAccelY.set (rawAngAccelVec [1])
        self.angAccelZ.set (rawAngAccelVec [2])
        
        self.angVelocX.set (self.angVelocX + self.angAccelX * world.period)
        self.angVelocY.set (self.angVelocY + self.angAccelY * world.period)
        self.angVelocZ.set (self.angVelocZ + self.angAccelZ * world.period)
        angVelocVec = radiansPerDegree * numpy.array ((self.angVelocX (), self.angVelocY (), self.angVelocZ ()))
        
        # Integration of rotation
        # Source: Friendly F# and C++ (fun with game physics), by Dr Giuseppe Maggiore and Dino Dini, May 22, 2014
        if useQuaternions:
            # Quaternions are much more numerically stable
            self._shipRotQuat = normized (self._shipRotQuat + quatMul (quatFromVec (angVelocVec), self._shipRotQuat) / 2 * world.period ())
            
            self.shipRotQuat0.set (self._shipRotQuat [0])
            self.shipRotQuat1.set (self._shipRotQuat [1])
            self.shipRotQuat2.set (self._shipRotQuat [2])
            self.shipRotQuat3.set (self._shipRotQuat [3])
            
            self._shipRotQuat [0] = self.shipRotQuat0 ()
            self._shipRotQuat [1] = self.shipRotQuat1 ()
            self._shipRotQuat [2] = self.shipRotQuat2 ()
            self._shipRotQuat [3] = self.shipRotQuat3 ()
            
            self._shipRotMat = rotMatFromQuat (self._shipRotQuat)        
        else:
            # N.B. The rotation matrix cannot be found by applying angular velocity in x, y and z direction successively
            self._shipRotMat = self._shipRotMat + numpy.cross (angVelocVec, self._shipRotMat, axisb = 0, axisc = 0) * world.period ()
            modifiedGramSchmidt (self._shipRotMat)
            
        rawAttitudeVec = getXyzAngles (self._shipRotMat)
        self.attitudeX.set (rawAttitudeVec [0])
        self.attitudeY.set (rawAttitudeVec [1])
        self.attitudeZ.set (rawAttitudeVec [2])
                
        self.part ('sweep time measurement')
        self.sweepMin.set (world.period, world.period < self.sweepMin)
        self.sweepMax.set (world.period, world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        