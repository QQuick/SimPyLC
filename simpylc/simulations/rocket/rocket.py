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

import numpy as np

import simpylc as sp

import common as cm

import transforms as tf

# General remarks:
# - The physical reality of precession indicates that rotation matrix cannot be
#   found by applying angular acceleration in x, y and z direction successively.
# - To avoid gimbal lock, non-unique Euler angles and numerical instability of
#   (modified) Gram Schmidt, the use of quaternions seems the simplest way to go.

class Rocket (sp.Module):
    def __init__ (self):
        sp.Module.__init__ (self)

        self.page ('rocket physics')
        
        self.group ('gimbal angle blue/yellow', True)
        self.blueYellowDelta = sp.Register ()
        self.blueYellowRoughAngle = sp.Register ()
        self.blueYellowAngle = sp.Register ()
        
        self.group ('thruster angle green/red') 
        self.greenRedDelta = sp.Register ()
        self.greenRedRoughAngle = sp.Register ()
        self.greenRedAngle = sp.Register ()
        
        self.group ('fuel throttle')
        self.throttleDelta = sp.Register ()
        self.throttlePercent = sp.Register ()
        self.thrust = sp.Register ()      
        
        self.group ('ship')
        self.shipMass = sp.Register (5000)
        self.effectiveRadius = sp.Register (0.15)
        self.effectiveHeight = sp.Register (1.5)
        self.thrusterTiltSpeed = sp.Register (30)
        self.thrusterMaxAngle = sp.Register (90)
        self.throttleSpeed = sp.Register (20)
        self.thrusterMaxForce = sp.Register (100000)
        
        self.group ('sweep time measurement')
        self.sweepMin = sp.Register (1000)
        self.sweepMax = sp.Register ()
        self.sweepWatch = sp.Timer ()
        self.run = sp.Runner ()        
        
        self.group ('linear accelleration', True)
        self.linAccelX = sp.Register ()
        self.linAccelY = sp.Register ()
        self.linAccelZ = sp.Register ()
        
        self.group ('linear velocity')
        self.linVelocX = sp.Register ()
        self.linVelocY = sp.Register ()
        self.linVelocZ = sp.Register ()
        
        self.group ('position')
        self.positionX = sp.Register ()
        self.positionY = sp.Register ()
        self.positionZ = sp.Register (cm.earthDiam / 2)
        
        self.group ('thrust in ship frame')
        self.forwardThrust = sp.Register ()
        self.blueYellowThrust = sp.Register ()
        self.greenRedThrust = sp.Register ()
        
        self.group ('thrust in world frame')
        self.thrustX = sp.Register ()
        self.thrustY = sp.Register ()
        self.thrustZ = sp.Register ()
        
        self.group ('angular acceleration', True)
        self.angAccelX = sp.Register ()
        self.angAccelY = sp.Register ()
        self.angAccelZ = sp.Register ()
        
        self.group ('angular velocity')
        self.angVelocX = sp.Register ()
        self.angVelocY = sp.Register ()
        self.angVelocZ = sp.Register ()
        
        self.group ('torques in ship frame')
        self.blueYellowTorque = sp.Register ()
        self.greenRedTorque = sp.Register ()
        
        self.group ('torques in world frame')
        self.torqueX = sp.Register ()
        self.torqueY = sp.Register ()
        self.torqueZ = sp.Register ()
                
        if cm.useQuaternions:
            self._shipRotQuat = sp.quatFromAxAng (np.array ((1, 0, 0)), 0)
        
            self.group ('ship rotation quaternion')
            self.shipRotQuat0 = sp.Register ()
            self.shipRotQuat1 = sp.Register ()
            self.shipRotQuat2 = sp.Register ()
            self.shipRotQuat3 = sp.Register ()
            self._shipRotMat = sp.rotMatFromQuat (self._shipRotQuat)
        else:
            self._shipRotMat = np.array ([   # Columns are tangent (front), normal (up) and binormal (starboard) of ship
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ])
                              
        self.group ('attitude')
        self.attitudeX = sp.Register ()
        self.attitudeY = sp.Register ()
        self.attitudeZ = sp.Register ()
        
        self.group ('earth gravity', True)
        self.distEarthSurf = sp.Register ()        
        self.earthGravX = sp.Register ()
        self.earthGravY = sp.Register ()
        self.earthGravZ = sp.Register ()
        
        self.group ('moon gravity')
        self.distMoonSurf = sp.Register ()
        self.moonGravX = sp.Register ()
        self.moonGravY = sp.Register ()
        self.moonGravZ = sp.Register ()
        
        self.group ('total force')
        self.totalForceX = sp.Register ()
        self.totalForceY = sp.Register ()
        self.totalForceZ = sp.Register ()
        
    def input (self):   
        self.part ('gimbal angle blue/yellow')
        self.blueYellowDelta.set (sp.world.control.blueYellowDelta)
        
        self.part ('thruster angle green/red')
        self.greenRedDelta.set (sp.world.control.greenRedDelta)
        
        self.part ('fuel throttle')
        self.throttleDelta.set (sp.world.control.throttleDelta)
        
    def sweep (self):
        self.part ('gimbal angle blue/yellow')
        self.blueYellowRoughAngle.set (
            sp.limit (
                self.blueYellowRoughAngle + self.blueYellowDelta * self.thrusterTiltSpeed * sp.world.period,
                self.thrusterMaxAngle
            )
        )
        self.blueYellowAngle.set (sp.snap (self.blueYellowRoughAngle, 0, 3))

        self.part ('thruster angle green/red')
        self.greenRedRoughAngle.set (
            sp.limit (
                self.greenRedRoughAngle + self.greenRedDelta * self.thrusterTiltSpeed * sp.world.period,
                self.thrusterMaxAngle
            )
        )
        self.greenRedAngle.set (sp.snap (self.greenRedRoughAngle, 0, 3))
        
        self.part ('fuel throttle')
        self.throttlePercent.set (
            sp.limit (
                self.throttlePercent + self.throttleDelta * self.throttleSpeed * sp.world.period,
                0,
                100
            )
        )
        self.thrust.set (self.throttlePercent * self.thrusterMaxForce / 100)

        self.part ('linear movement')
        
        thrusterForceVec = np.array ((0, 0, self.thrust ()))
        
        if cm.useQuaternions:
            thrusterRotQuat = sp.quatMul (
                sp.quatFromAxAng (np.array ((1, 0, 0)), self.blueYellowAngle),
                sp.quatFromAxAng (np.array ((0, 1, 0)), -self.greenRedAngle)
            )
            shipForceVec = sp.quatVecRot (thrusterRotQuat, thrusterForceVec)
        else:
            # Local coord sys, so "forward" order
            thrusterRotMat = tf.getRotXMat (self.blueYellowAngle) @ tf.getRotYMat (-self.greenRedAngle)    
            shipForceVec = thrusterRotMat @ thrusterForceVec
        
        self.forwardThrust.set (shipForceVec [2])
        self.blueYellowThrust.set (shipForceVec [1])
        self.greenRedThrust.set (shipForceVec [0])
        
        if cm.useQuaternions:
            worldForceVec = sp.quatVecRot (self._shipRotQuat, shipForceVec)
        else:
            worldForceVec = self._shipRotMat @ shipForceVec 
            
        self.thrustX.set (worldForceVec [0])
        self.thrustY.set (worldForceVec [1])
        self.thrustZ.set (worldForceVec [2])
             
        earthGravVec = cm.getGravVec (self.shipMass, cm.earthMass, cm.earthDiam, sp.tEva ((self.positionX, self.positionY, self.positionZ)))
        self.earthGravX.set (earthGravVec [0])
        self.earthGravY.set (earthGravVec [1])
        self.earthGravZ.set (earthGravVec [2])  
      
        moonGravVec = cm.getGravVec (self.shipMass, cm.moonMass, cm.moonDiam, sp.tSub (sp.tEva ((self.positionX, self.positionY, self.positionZ)), (0, 0, cm.earthMoonDist)))
        self.moonGravX.set (moonGravVec [0])
        self.moonGravY.set (moonGravVec [1])
        self.moonGravZ.set (moonGravVec [2])
        
        self.totalForceX.set (self.thrustX + self.earthGravX + self.moonGravX)
        self.totalForceY.set (self.thrustY + self.earthGravY + self.moonGravY)
        self.totalForceZ.set (self.thrustZ + self.earthGravZ + self.moonGravZ)
        
        self.linAccelX.set (self.totalForceX / self.shipMass)
        self.linAccelY.set (self.totalForceY / self.shipMass)
        self.linAccelZ.set (self.totalForceZ / self.shipMass)
        
        self.linVelocX.set (self.linVelocX + self.linAccelX * sp.world.period)
        self.linVelocY.set (self.linVelocY + self.linAccelY * sp.world.period)
        self.linVelocZ.set (self.linVelocZ + self.linAccelZ * sp.world.period)
        
        self.positionX.set (self.positionX + self.linVelocX * sp.world.period)
        self.positionY.set (self.positionY + self.linVelocY * sp.world.period)
        self.positionZ.set (self.positionZ + self.linVelocZ * sp.world.period)
        
        self.part ('angular movement')
        
        rSq = self.effectiveRadius * self.effectiveRadius
        hSq = self.effectiveHeight * self.effectiveHeight

        # Source: https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors        
        shipInertMat = self.shipMass () / 12 * np.array  (
            (
                ((3 * rSq + hSq) / 12   , 0                     , 0      ),
                (0                      , (3 * rSq + hSq) / 12  , 0      ),
                (0                      , 0                     , rSq / 6)
            )
        )
        invInertMat = np.linalg.inv (self._shipRotMat @ shipInertMat @ self._shipRotMat.T)
                
        self.blueYellowTorque.set (self.blueYellowThrust * self.effectiveHeight / 2)
        self.greenRedTorque.set (-self.greenRedThrust * self.effectiveHeight / 2)
        shipTorqueVec = np.array ((self.blueYellowTorque (), self.greenRedTorque (), 0))
        
        if cm.useQuaternions:
            rawTorqueVec = sp.quatVecRot (self._shipRotQuat, shipTorqueVec)
        else:
            rawTorqueVec = self._shipRotMat @ shipTorqueVec
        self.torqueX.set (rawTorqueVec [0])
        self.torqueY.set (rawTorqueVec [1])
        self.torqueZ.set (rawTorqueVec [2])
        torqueVec = np.array ((self.torqueX (), self.torqueY (), self.torqueZ ()))
        
        rawAngAccelVec = sp.degreesPerRadian * invInertMat @ torqueVec
        
        self.angAccelX.set (rawAngAccelVec [0])
        self.angAccelY.set (rawAngAccelVec [1])
        self.angAccelZ.set (rawAngAccelVec [2])
        
        self.angVelocX.set (self.angVelocX + self.angAccelX * sp.world.period)
        self.angVelocY.set (self.angVelocY + self.angAccelY * sp.world.period)
        self.angVelocZ.set (self.angVelocZ + self.angAccelZ * sp.world.period)
        angVelocVec = sp.radiansPerDegree * np.array ((self.angVelocX (), self.angVelocY (), self.angVelocZ ()))
        
        # Actual integration over one timestep
        # Source: Friendly F# and C++ (fun with game physics), by Dr Giuseppe Maggiore and Dino Dini, May 22, 2014
        if cm.useQuaternions:
            # Quaternions are much more numerically stable
            self._shipRotQuat = sp.normized (self._shipRotQuat + sp.quatMul (sp.quatFromVec (angVelocVec), self._shipRotQuat) / 2 * sp.world.period ())
            
            self.shipRotQuat0.set (self._shipRotQuat [0])
            self.shipRotQuat1.set (self._shipRotQuat [1])
            self.shipRotQuat2.set (self._shipRotQuat [2])
            self.shipRotQuat3.set (self._shipRotQuat [3])
            
            self._shipRotQuat [0] = self.shipRotQuat0 ()
            self._shipRotQuat [1] = self.shipRotQuat1 ()
            self._shipRotQuat [2] = self.shipRotQuat2 ()
            self._shipRotQuat [3] = self.shipRotQuat3 ()
            
            self._shipRotMat = sp.rotMatFromQuat (self._shipRotQuat)        
        else:
            # N.B. The rotation matrix cannot be found by applying angular velocity in x, y and z direction successively
            self._shipRotMat = self._shipRotMat + np.cross (angVelocVec, self._shipRotMat, axisb = 0, axisc = 0) * sp.world.period ()
            if cm.useGramSchmidt:
                tf.modifiedGramSchmidt (self._shipRotMat)
            
        rawAttitudeVec = tf.getXyzAngles (self._shipRotMat)
        self.attitudeX.set (rawAttitudeVec [0])
        self.attitudeY.set (rawAttitudeVec [1])
        self.attitudeZ.set (rawAttitudeVec [2])
                
        self.part ('sweep time measurement')
        self.sweepMin.set (sp.world.period, sp.world.period < self.sweepMin)
        self.sweepMax.set (sp.world.period, sp.world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)
        
