import sys as ss

ss.path.append ('..')

import time as tm
import math as mt

import socket as sc

import simpylc as sp

import socket_wrapper as sw
import vessel as vs
import almanac as an
import constants as cs

class Deckhand:
    def __init__ (self, crew):
        self.crew = crew

    def work (self, sweep):
        with sc.socket (*sw.socketType) as self.clientSocket:
            self.clientSocket.connect (sw.address)
            self.socketWrapper = sw.SocketWrapper (self.clientSocket)

            while True:
                self.input ()
                sweep ()
                self.output ()
                tm.sleep (0.02)

    def input (self):
        sensors = self.socketWrapper.recv ()

        self.courseAngle = sensors ['courseAngle']
        self.vaneAngle = sensors ['vaneAngle']
        self.lattitude = sensors ['lattitude']
        self.longitude = sensors ['longitude']

    def output (self):
        actuators = {
            'rudderAngle': self.rudderAngle,
            'sheetLength': self.sheetLength
        }

        self.socketWrapper.send (actuators)

    def getCurrentLocation (self):
        return self.lattitude, self.longitude

    def getCourseAngle (self):
        return an.symmetrize (self.courseAngle)

    def getVaneAngle (self):
        return an.symmetrize (self.vaneAngle)

    def setRudderAngle (self, rudderAngle):
        self.rudderAngle = an.symmetrize (rudderAngle)

    def setSailAngle (self, sailAngle):
        self.sheetLength = 2 * mt.sin (0.5 * abs (an.symmetrize (sailAngle)) * an.radianPerDegree) * cs.boomLength

    def holdPosition (self):
        self.sheetLength = cs.finity
