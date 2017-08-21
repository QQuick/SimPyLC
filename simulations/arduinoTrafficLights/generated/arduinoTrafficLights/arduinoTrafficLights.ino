// ======================== BEGIN OF GENERATED CODE ========================



// ====== BEGIN OF License COMMENT BLOCK, INCLUDE IN ANY COPY OF THIS GENERATED CODE AND DO NOT REMOVE ======
//
// I M P O R T A N T   S A F E T Y   N O T I C E
//
// THIS CODE IS INTENDED SOLELY FOR EDUCATIONAL PURPOSES AND IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS.
// IT IS STRICKTLY PROHIBITED TO USE THIS GENERATED CODE IN ANY SITUATION THAT ENTAILS RISK OF DAMAGE OR INJURIES.
//
// USE OF THIS CODE IS GOVERNED BY THE QQUICK LICENSE (WWW.QQUICK.ORG/LICENSE).
// YOUR LICENSE TO USE THIS GENERATED CODE AUTOMATICALLY ENDS IF YOU REMOVE OR LEAVE OUT THIS LICENSE COMMENT BLOCK OR THE CODE THAT GENERATED IT. 
//
// ====== END OF License COMMENT BLOCK, INCLUDE IN COPY OF THIS GENERATED CODE AND DO NOT REMOVE ======



// Generator: SimPyLC 3.6.0
// Generated: 2017-08-21 18:46:41.937185
// Target platform: Arduino



// ____________ General includes ____________

#include <math.h>



// ____________ Arduino macros ____________

#define getNowExact() micros ()
#define getNowInexact() millis ()



// ____________ General macros ____________

// Circuit operations

#define mark4(marker, trueValue, condition, falseValue) marker = (condition) ? (trueValue) : (falseValue)
#define mark3(marker, trueValue, condition) if (condition) marker = (trueValue)
#define mark2(marker, trueValue) marker = (trueValue)
#define mark1(marker) marker = True

#define trigger2(oneshot, condition) oneshot.value = oneshot.memo; oneshot.memo = (condition); oneshot.value = !oneshot.value and oneshot.memo
#define trigger1(oneshot) oneshot.value = !oneshot.memo; oneshot.memo = True
#define spiked1(oneshot) (oneshot.value)

#define latch2(latch, condition) if (condition) latch = True
#define latch1 (latch) latch = True

#define unlatch2(latch, condition) if (condition) latch = False
#define unlatch1 (latch) latch = False

#define set4(register, trueValue, condition, falseValue) register = (condition) ? (trueValue) : (falseValue)
#define set3(register, trueValue, condition) if (condition) register = (trueValue)
#define set2(register, trueValue) register = (trueValue)
#define set1(register) register = 1

#define reset2(timer, condition) if (condition) {timer.exact = nowExact; timer.inexact = nowInexact;}
#define reset1(timer) timer.exact = nowExact; timer.inexact = nowInexact
#define elapsed1(timer) ((nowInexact - timer.inexact) < 3.6e6 ? 1e-6 * (nowExact - timer.exact) : 1e-3 * (nowInexact - timer.inexact))

// Support operations

#define update()\
    thenExact = nowExact; nowExact = getNowExact(); period = 1e-6 * (nowExact - thenExact);\
    nowInexact = getNowInexact();\
    first = False;

// Types

#define False 0
#define True 1
#define Bool bool
#define UInt unsigned long
#define Int long
#define Float double
#define Marker int
#define Oneshot struct {int value; int memo;}
#define Latch int
#define Register double
#define Timer struct {unsigned long exact; unsigned long inexact;}

// Math operations

#define abs1(value) fabs (value)
#define max2(value0, value1) fmax (value0, value1)
#define min2(value0, value1) fmin (value0, value1)
#define limit3(value, aLimit0, aLimit1) min (max (value, aLimit0), aLimit1)  
#define limit2(value, aLimit) limit3 (value, -aLimit, aLimit)
#define digit2(value, index) getDigit (int (value), index)

// ____________ General functions ____________

int getDigit (int value, int index) {
    return (index == 0) ? value % 10 : getDigit (value / 10, --index);
}

// ____________ General variables ____________

UInt nowExact = 0;
UInt thenExact = 0;
UInt nowInexact = 0;
Float period = 1;
Bool first = True;



// ____________ PLC variables ____________

// ______ Module: trafficLights ______

// Page: Trafic lights

// Group: Timers

Timer regularPhaseTimer = {nowExact, nowInexact};
Timer cyclePhaseTimer = {nowExact, nowInexact};
Register tBlink = 0.3;
Timer blinkTimer = {nowExact, nowInexact};
Oneshot blinkPulse = {False, False};
Marker blink = False;

// Group: Mode switching

Marker modeButton = False;
Oneshot modePulse = {False, False};
Register modeStep = 0;
Marker regularMode = True;
Marker cycleMode = False;
Marker nightMode = False;
Marker offMode = False;

// Group: Night blinking

Marker allowRed = False;

// Group: Regular mode phases

Marker northSouthGreen = True;
Marker northSouthBlink = False;
Marker eastWestGreen = False;
Marker eastWestBlink = False;

// Group: Cycle mode phases

Marker northGreen = False;
Marker northBlink = False;
Marker eastGreen = False;
Marker eastBlink = False;
Marker southGreen = False;
Marker southBlink = False;
Marker westGreen = False;
Marker westBlink = False;

// Group: Lamps

Marker northGreenLamp = False;
Marker northRedLamp = False;
Marker eastGreenLamp = False;
Marker eastRedLamp = False;
Marker southGreenLamp = False;
Marker southRedLamp = False;
Marker westGreenLamp = False;
Marker westRedLamp = False;

// Group: Regular phase end times

Register tNorthSouthGreen = 5;
Register tNorthSouthBlink = 7;
Register tEastWestGreen = 12;
Register tEastWestBlink = 14;

// Group: Cycle phase end times

Register tNorthGreen = 5;
Register tNorthBlink = 7;
Register tEastGreen = 12;
Register tEastBlink = 14;
Register tSouthGreen = 19;
Register tSouthBlink = 21;
Register tWestGreen = 26;
Register tWestBlink = 28;

// Group: Street illumination

Marker brightButton = False;
Oneshot brightPulse = {False, False};
Marker brightDirection = True;
Register brightMin = 2047;
Register brightMax = 4095;
Register brightFluxus = 200;
Register brightDelta = 0;
Register streetLamp = 2047;

// Group: System




// ____________ PLC cycle ____________

void cycle () {

	// ______ Module: trafficLights ______

	// ___ Sweep ___

	// Part: Timers

	reset2 (regularPhaseTimer, ((elapsed1 (regularPhaseTimer) > tEastWestBlink) || cycleMode || nightMode || offMode));
	reset2 (cyclePhaseTimer, ((elapsed1 (cyclePhaseTimer) > tWestBlink) || regularMode || nightMode || offMode));
	reset2 (blinkTimer, (elapsed1 (blinkTimer) > tBlink));
	trigger2 (blinkPulse, (elapsed1 (blinkTimer) == 0));
	mark3 (blink, (!blink), spiked1 (blinkPulse));

	// Part: Mode switching

	trigger2 (modePulse, modeButton);
	set3 (modeStep, ((Int) (modeStep + 1) % (Int) 4), spiked1 (modePulse));
	mark2 (regularMode, (modeStep == 0));
	mark2 (cycleMode, (modeStep == 1));
	mark2 (nightMode, (modeStep == 2));
	mark2 (offMode, (modeStep == 3));

	// Part: Regular mode phases

	mark2 (northSouthGreen, (0 < elapsed1 (regularPhaseTimer) && elapsed1 (regularPhaseTimer) < tNorthSouthGreen));
	mark2 (northSouthBlink, (tNorthSouthGreen < elapsed1 (regularPhaseTimer) && elapsed1 (regularPhaseTimer) < tNorthSouthBlink));
	mark2 (eastWestGreen, (tNorthSouthBlink < elapsed1 (regularPhaseTimer) && elapsed1 (regularPhaseTimer) < tEastWestGreen));
	mark2 (eastWestBlink, (tEastWestGreen < elapsed1 (regularPhaseTimer)));

	// Part: Cycle mode phases

	mark2 (northGreen, (0 < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tNorthGreen));
	mark2 (northBlink, (tNorthGreen < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tNorthBlink));
	mark2 (eastGreen, (tNorthBlink < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tEastGreen));
	mark2 (eastBlink, (tEastGreen < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tEastBlink));
	mark2 (southGreen, (tEastBlink < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tSouthGreen));
	mark2 (southBlink, (tSouthGreen < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tSouthBlink));
	mark2 (westGreen, (tSouthBlink < elapsed1 (cyclePhaseTimer) && elapsed1 (cyclePhaseTimer) < tWestGreen));
	mark2 (westBlink, (tWestGreen < elapsed1 (cyclePhaseTimer)));

	// Part: Night blinking

	mark2 (allowRed, (regularMode || cycleMode || (nightMode && blink)));

	// Part: Traffic lamps

	mark2 (northGreenLamp, (northSouthGreen || northGreen || ((northSouthBlink || northBlink) && blink)));
	mark2 (northRedLamp, ((!(northSouthGreen || northGreen || northSouthBlink || northBlink)) && allowRed));
	mark2 (eastGreenLamp, (eastWestGreen || eastGreen || ((eastWestBlink || eastBlink) && blink)));
	mark2 (eastRedLamp, ((!(eastWestGreen || eastGreen || eastWestBlink || eastBlink)) && allowRed));
	mark2 (southGreenLamp, (northSouthGreen || southGreen || ((northSouthBlink || southBlink) && blink)));
	mark2 (southRedLamp, ((!(northSouthGreen || southGreen || northSouthBlink || southBlink)) && allowRed));
	mark2 (westGreenLamp, (eastWestGreen || westGreen || ((eastWestBlink || westBlink) && blink)));
	mark2 (westRedLamp, ((!(eastWestGreen || westGreen || eastWestBlink || westBlink)) && allowRed));

	// Part: Street illumination

	trigger2 (brightPulse, brightButton);
	mark3 (brightDirection, (!brightDirection), spiked1 (brightPulse));
	set4 (brightDelta, ((-brightFluxus) * period), brightDirection, (brightFluxus * period));
	set3 (streetLamp, limit3 ((streetLamp + brightDelta), brightMin, brightMax), brightButton);

    // ______ System ______

    update ();
}



// ======================== END OF GENERATED CODE ========================



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
