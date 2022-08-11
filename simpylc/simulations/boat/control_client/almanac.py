'''
Lattitude and longitude are in signed decimal degrees: -90 (south) <= lattitude <= 90 (north), -180 (west) <= longitude <= 180 (east)
The x axis points to the east, the y axis points to the north.
Polar expeditions are not yet) supported.
'''

import os
import math as mt

import constants as cs

degreePerRadian = 180 / mt.pi
radianPerDegree = 1 / degreePerRadian

waypointsFilename = f'{os.path.dirname (os.path.abspath (__file__))}/{cs.waypointsFilename}'
boomLength = 0.5

maxSegmentSpan = 10         # Max step for lattitude and longitude [degree]
targetMargin = 5            # Margin allowed in passing a waypoint [m]
earthPerimeter = 4.0075e7   # On average, high accuracy not needed [m]
meterPerDegreeLattitude = earthPerimeter / 360

def getMeterPerDegreeLongitude (lattitude):
    return earthPerimeter * mt.cos (lattitude * radianPerDegree) / 360

class Exclude:
    def __init__ (self, absThreshold):
        self.absThreshold = absThreshold
        self.alteredValue = 0

    def __call__ (self, value):
        if abs (value) >= self.absThreshold:
            self.alteredValue = 0
            return value
        else:
            if self.alteredValue == 0:
                if value >= 0:
                    self.alteredValue = self.absThreshold
                else:
                    self.alteredValue = -self.absThreshold
            return self.alteredValue

def asymmetrize (angle):
    return angle % 360                              # 0 <= asym < 360

def symmetrize (angle):
    return 180 - asymmetrize (180 - angle)     # -180 < sym <= 180

class SegmentSpanException (Exception):
    def __init__ (self, componentName):
        super () .__init__ (f'Error: Segment spans a {componentName} difference > {maxSegmentSpan} degrees')

def getWaypoints ():
        return [
            [float (item) for item in line.split ()]
        for line in open (waypointsFilename) .readlines () if not line.startswith ('#')
    ]  # Waypoints are absolute (lattitude: <-180, 180], longitude: [-90, 90]) pairs in decimal degrees

def getLeg (baseWaypoint, targetWaypoint):
    baseLattitude = baseWaypoint [0]
    targetLattitude = targetWaypoint [0]
    lattitudeDifference = targetLattitude - baseLattitude
    legY = meterPerDegreeLattitude * lattitudeDifference

    baseLongitude = baseWaypoint [1]
    targetLongitude = targetWaypoint [1]
    longitudeDifference = targetLongitude - baseLongitude

    '''
    if abs (longitudeDifference)  > maxSegmentSpan:
        raise SegmentSpanException ('longitude')
    '''

    if longitudeDifference < -180:
        longitudeDifference += 360
    elif longitudeDifference > 180:
        longitudeDifference -= 360

    '''
    if abs (longitudeDifference)  > maxSegmentSpan:
        raise SegmentSpanException ('lattitude')
    '''

    averageLattitude = (baseLattitude + targetLattitude) / 2
    legX = getMeterPerDegreeLongitude (averageLattitude) * longitudeDifference

    return legX, legY

def getLegAngle (leg):
    return symmetrize (degreePerRadian * mt.atan2 (leg [1], leg [0]) - 90)

def getLegLength (leg):
    return mt.sqrt (leg [0] ** 2 + leg [1] ** 2)

def getPosition (previousPosition, velocity, deltaTime):
    previousLattitude = previousPosition [0]
    newLattitude = previousLattitude + velocity [1] * deltaTime / meterPerDegreeLattitude
    averageLattitude = (previousLattitude + newLattitude) / 2
    previousLongitude = previousPosition [1]
    newLongitude = previousLongitude + velocity [0] * deltaTime / getMeterPerDegreeLongitude (averageLattitude)
    return newLattitude, newLongitude

def clip (value, maxAbsValue):
    return min (max (value, -maxAbsValue), maxAbsValue)

