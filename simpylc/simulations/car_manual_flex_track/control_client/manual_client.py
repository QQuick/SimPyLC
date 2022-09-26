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
import curses as cs

ss.path +=  [os.path.abspath (relPath) for relPath in  ('..',)] 

import socket_wrapper as sw
import parameters as pm

class ManualClient:
    def __init__ (self):
        self.steeringAngle = 0
        self.targetVelocity = 0

        self.io = cs.initscr () # take over terminal
        cs.noecho () # do not update terminal
        cs.cbreak () # set direct mode (no enter needed)
        self.io.keypad (True) # convert to key codes

        with open (pm.sampleFileName, 'w') as self.sampleFile:
            with sc.socket (*sw.socketType) as self.clientSocket:
                self.clientSocket.connect (sw.address)
                self.socketWrapper = sw.SocketWrapper (self.clientSocket)
                self.halfApertureAngle = False

                while True:
                    self.input ()
                    self.process ()
                    self.output ()
                    self.logTraining ()
                    tm.sleep (0.02)

    def input (self):
        sensors = self.socketWrapper.recv ()

        if not self.halfApertureAngle:
            self.halfApertureAngle = sensors ['halfApertureAngle']
            self.sectorAngle = 2 * self.halfApertureAngle / pm.lidarInputDim
            self.halfMiddleApertureAngle = sensors ['halfMiddleApertureAngle']
            
        if 'lidarDistances' in sensors:
            self.lidarDistances = sensors ['lidarDistances']
        else:
            self.sonarDistances = sensors ['sonarDistances']
    
    def process (self):
        key = self.io.getch ()
        if key == cs.KEY_UP:
            self.targetVelocity += pm.speedDelta
        elif key == cs.KEY_DOWN:
            self.targetVelocity -= pm.speedDelta
        elif key == cs.KEY_RIGHT:
            self.steeringAngle += pm.steerDelta
        elif key == cs.KEY_LEFT:
            self.steeringAngle -= pm.steerDelta

    def output (self):
        actuators = {
            'steeringAngle': self.steeringAngle,
            'targetVelocity': self.targetVelocity
        }

        self.socketWrapper.send (actuators)

    def logLidarTraining (self):
        sample = [pm.finity for entryIndex in range (pm.lidarInputDim + 1)]

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle):
            sectorIndex = round (lidarAngle / self.sectorAngle)
            sample [sectorIndex] = min (sample [sectorIndex], self.lidarDistances [lidarAngle])

        sample [-2] = self.steeringAngle
        sample [-1] = self.targetVelocity
        print (*sample, file = self.sampleFile)

    def logSonarTraining (self):
        sample = [pm.finity for entryIndex in range (pm.sonarInputDim + 1)]

        for entryIndex, sectorIndex in ((2, -1), (0, 0), (1, 1)):
            sample [entryIndex] = self.sonarDistances [sectorIndex]

        sample [-2] = self.steeringAngle
        sample [-1] = self.targetVelocity
        print (*sample, file = self.sampleFile)

    def logTraining (self):
        if hasattr (self, 'lidarDistances'):
            self.logLidarTraining ()
        else:
            self.logSonarTraining ()

ManualClient ()
