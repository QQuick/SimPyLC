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

void setup () {
    analogWriteResolution (12);

    pinMode (33, OUTPUT); pinMode (35, OUTPUT); pinMode (37, OUTPUT); pinMode (39, OUTPUT);
    pinMode (41, OUTPUT); pinMode (43, OUTPUT); pinMode (45, OUTPUT); pinMode (47, OUTPUT);
    pinMode (49, INPUT); pinMode (51, INPUT);
}

void loop () {
    modeButton = !digitalRead (49); brightButton = !digitalRead (51);

    cycle ();

    digitalWrite (39, northGreenLamp); digitalWrite (41, northRedLamp);
    digitalWrite (35, eastGreenLamp); digitalWrite (37, eastRedLamp);
    digitalWrite (47, southGreenLamp); digitalWrite (33, southRedLamp);
    digitalWrite (43, westGreenLamp); digitalWrite (45, westRedLamp);

    analogWrite (DAC0, streetLamp);
}       
