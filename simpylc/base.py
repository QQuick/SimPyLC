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

import os
from math import *
from inspect import *

programName = 'SimPyLC'
programVersion = '3.9.7'
programNameAndVersion = '{0} {1}'.format (programName, programVersion)
programDir = os.getcwd () .replace ('\\', '/') .rsplit ('/', 3) [-1]

def getTitle (name):
    return '{0} - {1} - {2}' .format (programDir, name, programNameAndVersion)  
      
def evaluate (anObject):
    if hasattr (anObject, '__call__'):
        return anObject ()
    else:
        return anObject      
      
def tEva (v):
    return tuple (evaluate (entry) for entry in v)
                
def tNeg (v):
    return tuple (-entry for entry in v)
    
def tAdd (v0, v1):
    return tuple (entry0 + entry1 for entry0, entry1 in zip (v0, v1))
    
def tSub (v0, v1):
    return tuple (entry0 - entry1 for entry0, entry1 in zip (v0, v1))
        
def tMul (v0, v1):
    return tuple (entry0 * entry1 for entry0, entry1 in zip (v0, v1))

def tsMul (v, x):
    return tuple (entry * x for entry in v)
    
def tDiv (v, x):
    return tuple (entry0 / entry1 for entry0, entry1 in zip (v0, v1))

def tsDiv (v, x):
    return tuple (entry / x for entry in v)
   
def tNor (v):
    return sqrt (sum (entry * entry for entry in v))
    
def tUni (v):
    return tsDiv (v, tNor (v))
            
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
    
def getFileLineClause (frame):
    frameInfo = getframeinfo (frame)
    return f'in file {frameInfo.filename}, line {frameInfo.lineno}:'
    
def abort ():
    input ()
    exit ()
    
def abortUnderConstruction (frame):
    print ()
    print ('ERROR', getFileLineClause (frame), 'This simulation is under construction')
    print ()
    abort ()
    
def warnDeprecated (frame, featureOld, featureNew = None):
    print ()
    print ('WARNING', getFileLineClause (frame), featureOld [0].upper () + featureOld [1:], 'will be removed in future versions of', programName, end = '')
    if featureNew:
        print (', please use', featureNew, 'instead')
    else:
        print ()
        
def warnAsyncTrack (frame):
    print ()
    print ('WARNING', getFileLineClause (frame), 'Instance recycling in display function may cause \'jumpy\' camera tracking')

        
