 /**
Copyright (C) 2013 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicence for details.

The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html

 __________________________________________________________________________
 

 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your licence.
**/

// Pins configured for Arduino Due, adapt for Uno
        
int dataPin = 22, clockPin = 24, latchPin = 26;
int powerPin = 28, childLockPin = 30, plateSelectPin = 32;
int upPin = 34, downPin = 36, alarmSelectPin = 38;
int plate0Pin = 2, plate1Pin = 3, plate2Pin = 4, plate3Pin = 5;
int buzzerPin = 40;

int gain = 255 / 9;

int dark = 0, g = 1, f = 2, e = 4, d = 8, c = 16, b = 32, a = 64, dot = 128;

int segments [] = {
    a + b + c + d + e + f,
    b + c,
    a + b + g + e + d,
    a + b + g + c + d,
    f + g + b + c,
    a + f + g + c + d,
    a + f + e + d + c + g,
    a + b + c,
    a + b + c + d + e + f + g,
    g + f + a + b + c + d
};

void setup () {
    pinMode (dataPin, OUTPUT); pinMode(clockPin, OUTPUT); pinMode(latchPin, OUTPUT);
    pinMode (powerPin, INPUT); pinMode (childLockPin, INPUT); pinMode (plateSelectPin, INPUT);
    pinMode (upPin, INPUT); pinMode (downPin, INPUT); pinMode (alarmSelectPin, INPUT);
    pinMode (plate0Pin, OUTPUT); pinMode (plate1Pin, OUTPUT); pinMode (plate2Pin, OUTPUT); pinMode (plate3Pin, OUTPUT);
    pinMode (buzzerPin, OUTPUT);
}

void readInputs () {
    powerButton = digitalRead (powerPin); childLockButton = digitalRead (childLockPin); plateSelectButton = digitalRead (plateSelectPin);
    upButton = digitalRead (upPin); downButton = digitalRead (downPin); alarmSelectButton = digitalRead (alarmSelectPin);
}

void writeOutputs () {  
    analogWrite (plate0Pin, gain * plate0Temp); analogWrite (plate1Pin, gain * plate1Temp);
    analogWrite (plate2Pin, gain * plate2Temp); analogWrite (plate3Pin, gain * plate3Temp);
    digitalWrite (buzzerPin, buzzer);
    
    digitalWrite (latchPin, 0);
    shiftOut (dataPin, clockPin, LSBFIRST, 1 << int (3 - digitIndex));
    shiftOut (dataPin, clockPin, LSBFIRST, ~(power ? (segments [int (digitValue)] + (digitDot ? dot : dark)) : dark)); // Active low    
    digitalWrite (latchPin, 1);
}

void loop () {
    readInputs ();
    cycle ();
    writeOutputs ();
}
