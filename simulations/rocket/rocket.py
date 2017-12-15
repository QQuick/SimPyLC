# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software./
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
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
        self.thrusterForce = Register ()      
        
        self.group ('ship')
        self.totalMass = Register (5000)
        self.effectiveRadius = Register (0.15)
        self.effectiveHeight = Register (1.5)
        self.thrusterTiltSpeed = Register (30)
        self.thrusterMaxAngle = Register (90)
        self.throttleSpeed = Register (20)
        self.thrusterMaxForce = Register (10000)
        
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
        self.positionZ = Register ()
        
        self.group ('Forces in ship frame')
        self.forwardForce = Register ()
        self.blueYellowForce = Register ()
        self.greenRedForce = Register ()
        
        self.group ('Forces in world frame')
        self.forceX = Register ()
        self.forceY = Register ()
        self.forceZ = Register ()        
        
        self.group ('angular acceleration', True)
        self.angAccelX = Register ()
        self.angAccelY = Register ()
        self.angAccelZ = Register ()
        
        self.group ('angular velocity')
        self.angVelocX = Register ()
        self.angVelocY = Register ()
        self.angVelocZ = Register ()
        
        self.group ('ship rot quat')
        self.srq0 = Register ()
        self.srq1 = Register ()
        self.srq2 = Register ()
        self.srq3 = Register ()
        
        self.group ('attitude')
        self.axisX = Register ()
        self.axisY = Register ()
        self.axisZ = Register ()
        self.angle = Register ()
        
        self.group ('Torques in ship frame')
        self.blueYellowTorque = Register ()
        self.greenRedTorque = Register ()
        
        self.group ('Torques in world frame')
        self.torqueX = Register ()
        self.torqueY = Register ()
        self.torqueZ = Register ()
        
        # Auxiliary attributes
        
        self._shipRotQuat = quatFromAxAng (numpy.array ((1, 0, 0)), 0)
        
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
        self.thrusterForce.set (self.throttlePercent * self.thrusterMaxForce / 100)

        self.part ('linear movement')
        
        thrusterRotQuat = quatMul (
            quatFromAxAng (numpy.array ((1, 0, 0)), self.blueYellowAngle),
            quatFromAxAng (numpy.array ((0, 1, 0)), -self.greenRedAngle)
        )
        
        thrusterForceVec = numpy.array ((0, 0, self.thrusterForce ()))
        shipForceVec = quatVecRot (thrusterRotQuat, thrusterForceVec)
        
        self.forwardForce.set (shipForceVec [2])
        self.blueYellowForce.set (shipForceVec [1])
        self.greenRedForce.set (shipForceVec [0])
        
        worldForceVec = quatVecRot (self._shipRotQuat, shipForceVec)
        self.forceX.set (worldForceVec [0])
        self.forceY.set (worldForceVec [1])
        self.forceZ.set (worldForceVec [2])
                
        self.linAccelX.set (self.forceX / self.totalMass)
        self.linAccelY.set (self.forceY / self.totalMass)
        self.linAccelZ.set (self.forceZ / self.totalMass)
        
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
        shipInertMat = self.totalMass () / 12 * numpy.array  (
            (
                ((3 * rSq + hSq) / 12   , 0                     , 0      ),
                (0                      , (3 * rSq + hSq) / 12  , 0      ),
                (0                      , 0                     , rSq / 6)
            )
        )

        inertMat = quatMatRot (self._shipRotQuat, shipInertMat)
        
        self.blueYellowTorque.set (self.blueYellowForce * self.effectiveHeight / 2)
        self.greenRedTorque.set (-self.greenRedForce * self.effectiveHeight / 2)
        shipTorqueVec = numpy.array ((self.blueYellowTorque (), self.greenRedTorque (), 0))
        
        rawTorqueVec = quatVecRot (self._shipRotQuat, shipTorqueVec)
        self.torqueX.set (rawTorqueVec [0])
        self.torqueY.set (rawTorqueVec [1])
        self.torqueZ.set (rawTorqueVec [2])
        torqueVec = numpy.array ((self.torqueX (), self.torqueY (), self.torqueZ ()))
        
        rawAngAccelVec = degreesPerRadian * numpy.linalg.inv (inertMat) @ torqueVec
        self.angAccelX.set (rawAngAccelVec [0])
        self.angAccelY.set (rawAngAccelVec [1])
        self.angAccelZ.set (rawAngAccelVec [2])
        
        self.angVelocX.set (self.angVelocX + self.angAccelX * world.period)
        self.angVelocY.set (self.angVelocY + self.angAccelY * world.period)
        self.angVelocZ.set (self.angVelocZ + self.angAccelZ * world.period)
        angVelocVec = radiansPerDegree * numpy.array ((self.angVelocX (), self.angVelocY (), self.angVelocZ ()))
        
        # Source: Friendly F# and C++ (fun with game physics), by Dr Giuseppe Maggiore and Dino Dini, May 22, 2014
        #print (self._shipRotQuat)
        self._shipRotQuat += quatMul (quatFromVec (angVelocVec), self._shipRotQuat) / 2 * world.period ()
        #print (self._shipRotQuat)
        #print ('--------------------')
        
        normize (self._shipRotQuat)        
        
        self.srq0.set (self._shipRotQuat [0])
        self.srq1.set (self._shipRotQuat [1])
        self.srq2.set (self._shipRotQuat [2])
        self.srq3.set (self._shipRotQuat [3])
        
        axis, angle = axAngFromQuat (self._shipRotQuat)
        self.axisX.set (axis [0])
        self.axisY.set (axis [1])
        self.axisZ.set (axis [2])   
        self.angle.set (angle)
        
        
        axis [0] = self.axisX ()
        axis [1] = self.axisY ()
        axis [2] = self.axisZ ()
        angle = self.angle ()
        #self._shipRotQuat = quatFromAxAng (axis, angle)
        
        self.part ('sweep time measurement')
        self.sweepMin.set (world.period, world.period < self.sweepMin)
        self.sweepMax.set (world.period, world.period > self.sweepMax)
        self.sweepWatch.reset (self.sweepWatch > 2)
        self.sweepMin.set (1000, not self.sweepWatch)