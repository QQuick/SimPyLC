# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
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

import os

programName = 'SimPyLC'
programVersion = '3.5.4'
programNameAndVersion = '{0} {1}'.format (programName, programVersion)
programDir = os.getcwd () .replace ('\\', '/') .rsplit ('/', 3) [-1]

def getTitle (name):
    return '{0} - {1} - {2}' .format (programDir, name, programNameAndVersion)  

def evaluate (anObject):
    if hasattr (anObject, '__call__'):
        return anObject ()
    else:
        return anObject
            
class ColorsHex:
    def __init__ (self):
        self.panelBackgroundColor = '#000000'
        
        self.pageCaptionForegroundColor = '#bbffbb'
        self.pageCaptionBackgroundColor = self.panelBackgroundColor
        
        self.groupCaptionForegroundColor = '#bbffbb'
        self.groupCaptionBackgroundColor = self.panelBackgroundColor
        
        self.labelForegroundColor = '#aaaaaa'
        self.labelBackgroundColor = self.panelBackgroundColor
        
        self.entryReleasedForegroundColor = '#00ff00'
        self.entryReleasedBackgroundColor = '#002200'
        self.entryEditForegroundColor = '#bbbbff'
        self.entryEditBackgroundColor = '#000022'
        self.entryForcedForegroundColor = '#ffaa00'
        self.entryForcedBackgroundColor = '#331100'
        
        self.white = '#ffffff'
        self.silver = '#c0c0c0'
        self.gray = '#808080'
        self.black = '#000000'
        self.red = '#ff0000'
        self.maroon = '#800000'
        self.yellow = '#ffff00'
        self.olive = '#808000'
        self.lime = '#00ff00'
        self.green = '#008000'
        self.aqua = '#00ffff'
        self.teal = '#008080'
        self.blue = '#0000ff'
        self.navy = '#000080'
        self.fuchsia = '#ff00ff'
        self.purple = '#800080'
    
colorsHex = ColorsHex ()

for varName in vars (colorsHex):
    vars () [varName + 'Hex'] = getattr (colorsHex, varName)
        
for varName in vars (colorsHex):
    colorHex = getattr (colorsHex, varName) [1:]
    vars () [varName] = (int (colorHex [0:2], 16) / 255., int (colorHex [2:4], 16) / 255., int (colorHex [4:6], 16) / 255.)
    
def hexFromRgb (rgb):
    rgb = (int (255 * rgb [0]), int (255 * rgb [1]), int (255 * rgb [2]))
    return '#{:02x}{:02x}{:02x}'.format (*rgb)
    
backgroundColorFactor = 0.25

def backgroundFromRgb (rgb):
    return (backgroundColorFactor * rgb [0], backgroundColorFactor * rgb [1], backgroundColorFactor * rgb [2])
    
def decapitalize (aString):
    return aString [0] .lower () + aString [1:] if aString else ''
    
def underConstruction ():
    print ('THIS SIMULATION IS UNDER CONSTRUCTION')
    input ()
    exit ()
