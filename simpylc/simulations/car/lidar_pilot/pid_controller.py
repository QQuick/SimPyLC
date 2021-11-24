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

'''
Requirements:
=============

Given a timedependent reference signal and a timedependent feedback sensor input,
the PID controller should minimize the difference between them.
To this end it's output will be the sum of:
- A term proportional to this difference
- A term proportional the time integral of this difference
- A term proportional to the time derivative of this difference
The weight of this terms should be freely choosable when creating a PID controller.
The PID controller will function in a control loop with known, but varying cycle time.

Testspec:
=========

A number known time dependent signals will be fed to the PID controller.
They will be shown graphically together with the output of the controller,
allowing visual validation.

Design:
=======

The PID controller will be coded as a class,
receiving the p, i and d factors at construction time.
Construction happens prior to entering the control loop.
In the control loop, the output signal will be computed by a method of the controller,
receiving:
- The most recent cycle time
- The reference signal
- The feedback signal from the sensor
'''

class PidController:
    def __init__ (self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.yI = 0
        self.xErrorOld = 0

    def getY (self, deltaT, xSetpoint, xActual):
        
        # Deviation between setpoint and actual signal
        xError = xSetpoint - xActual
        
        # Proportional term
        yP = self.p * xError
        
        # Integrating term
        self.yI += self.i * xError * deltaT
        
        # Differentiating term
        yD = self.d * (xError - self.xErrorOld) / deltaT
        self.xErrorOld = xError
        
        # Summation
        return yP + self.yI + yD
    
