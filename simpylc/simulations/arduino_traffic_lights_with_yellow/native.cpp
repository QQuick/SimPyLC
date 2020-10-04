/*
Copyright (C) 2013 - 2020 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicence for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html
__________________________________________________________________________


THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your licence.
*/

// Pin assignment for Arduino Uno

void setup () {    
    pinMode (3, INPUT_PULLUP); pinMode (4, INPUT_PULLUP);

    pinMode (A0, OUTPUT); pinMode (A1, OUTPUT); pinMode (A2, OUTPUT);
    pinMode (A3, OUTPUT); pinMode (A4, OUTPUT); pinMode (A5, OUTPUT);
    pinMode (7, OUTPUT); pinMode (8, OUTPUT); pinMode (9, OUTPUT);
    pinMode (10, OUTPUT); pinMode (11, OUTPUT); pinMode (12, OUTPUT);
    
    pinMode (5, OUTPUT);
}

void loop () {
    modeButton = !digitalRead (3); brightButton = !digitalRead (4);

    cycle ();

    digitalWrite (A0, northGreenLamp); digitalWrite (A1, northYellowLamp); digitalWrite (A2, northRedLamp);
    digitalWrite (A3, eastGreenLamp); digitalWrite (A4, eastYellowLamp); digitalWrite (A5, eastRedLamp);
    digitalWrite (7, southGreenLamp); digitalWrite (8, southYellowLamp); digitalWrite (9, southRedLamp);
    digitalWrite (10, westGreenLamp); digitalWrite (11, westYellowLamp); digitalWrite (12, westRedLamp);

    analogWrite (5, (streetLamp - brightMin) / 16);
        

}       
