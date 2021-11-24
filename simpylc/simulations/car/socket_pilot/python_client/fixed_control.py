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

import time as tm
import traceback as tb
import math as mt
import sys as ss
import os
import socket as sc

ss.path +=  [os.path.abspath (relPath) for relPath in  ('..',)] 

import socket_wrapper as sw

finity = 1e20

class FixedControl:
    def __init__ (self):
        self.steeringAngle = 0

        with sc.socket (*sw.socketType) as self.clientSocket:
            self.clientSocket.connect (sw.address)
            self.socketWrapper = sw.SocketWrapper (self.clientSocket)
            self.lidarHalfApertureAngle = False

            while True:
                tm.sleep (0.02)
                self.input ()
                self.sweep ()
                self.output ()

    def input (self):
        sensors = self.socketWrapper.recv ()
        self.lidarDistances = sensors ['lidarDistances']

        if not self.lidarHalfApertureAngle:
            self.lidarHalfApertureAngle = sensors ['lidarHalfApertureAngle']
            
    def sweep (self):
        self.nearestObstacleDistance = finity
        self.nearestObstacleAngle = 0
        
        self.nextObstacleDistance = finity
        self.nextObstacleAngle = 0

        for lidarAngle in range (-self.lidarHalfApertureAngle, self.lidarHalfApertureAngle):
            lidarDistance = self.lidarDistances [lidarAngle]
            
            if lidarDistance < self.nearestObstacleDistance:
                self.nextObstacleDistance =  self.nearestObstacleDistance
                self.nextObstacleAngle = self.nearestObstacleAngle
                
                self.nearestObstacleDistance = lidarDistance 
                self.nearestObstacleAngle = lidarAngle

            elif lidarDistance < self.nextObstacleDistance:
                self.nextObstacleDistance = lidarDistance
                self.nextObstacleAngle = lidarAngle
           
        self.targetObstacleDistance = (self.nearestObstacleDistance + self.nextObstacleDistance) / 2

        self.steeringAngle = (self.nearestObstacleAngle + self.nextObstacleAngle) / 2
        self.targetVelocity = (90 - abs (self.steeringAngle)) / 60

    def output (self):
        actuators = {
            'steeringAngle': self.steeringAngle,
            'targetVelocity': self.targetVelocity
        }

        self.socketWrapper.send (actuators)

FixedControl ()
