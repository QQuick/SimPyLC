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



// Generator: SimPyLC 3.6.1
// Generated: 2017-11-23 16:36:32.384396
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

// ______ Module: control ______

// Page: Four plate stove control with cooking alarm

// Group: General buttons

Marker powerButton = False;
Oneshot powerEdge = {False, False};
Marker power = False;
;
Marker childLockButton = False;
Timer childLockChangeTimer = {nowExact, nowInexact};
Oneshot childLockEdge = {False, False};
Marker childLock = False;
Marker unlocked = False;

// Group: Plate selection

Marker plateSelectButton = False;
Oneshot plateSelectEdge = {False, False};
Register plateSelectDelta = 0;
Register plateSelectNr = 0;
Register tempDelta = 0;
Marker tempChange = False;

// Group: Up/down buttons

Marker upButton = False;
Oneshot upEdge = {False, False};
;
Marker downButton = False;
Oneshot downEdge = {False, False};

// Group: Cooking plates

Register plate0Temp = 0;
Marker plate0Selected = False;
;
Register plate1Temp = 0;
Marker plate1Selected = False;
;
Register plate2Temp = 0;
Marker plate2Selected = False;
;
Register plate3Temp = 0;
Marker plate3Selected = False;

// Group: Alarm selection button

Marker alarmSelectButton = False;
Oneshot alarmSelectEdge = {False, False};
Marker alarmSelected = False;
Register alarmTime = 0;
Timer alarmTimer = {nowExact, nowInexact};
Latch alarmOn = False;
Oneshot alarmEdge = {False, False};
Register alarmTimeLeft = 0;
Timer alarmChangeTimer = {nowExact, nowInexact};
Register alarmChangeStep = 0;
Register alarmDelta = 0;

// Group: Numerical displays

Register digitIndex = 0;
Register plateDigitValue = 0;
Register alarmDigitValue = 0;
Register digitValue = 0;
Marker digitDot = False;

// Group: Buzzer

Register buzzerOnTime = 6;
Timer buzzerOnTimer = {nowExact, nowInexact};
Latch buzzerOn = False;
Register buzzerBaseFreq = 300.0;
Timer buzzerPitchTimer = {nowExact, nowInexact};
Register buzzerFreq = 0;
Timer buzzerWaveTimer = {nowExact, nowInexact};
Oneshot buzzerEdge = {False, False};
Marker buzzer = False;

// Group: System

Register sweepMin = 1000;
Register sweepMax = 0;
Timer sweepWatch = {nowExact, nowInexact};



// ____________ PLC cycle ____________

void cycle () {

	// ______ Module: control ______

	// ___ Sweep ___

	// Part: Edge triggering of buttons

	trigger2 (powerEdge, powerButton);
	mark3 (power, (!power), ((!childLock) && spiked1 (powerEdge)));
	reset2 (childLockChangeTimer, (!(power && childLockButton)));
	trigger2 (childLockEdge, (elapsed1 (childLockChangeTimer) > 5));
	mark3 (childLock, (!childLock), spiked1 (childLockEdge));
	mark2 (unlocked, (power && (!childLock)));
	trigger2 (plateSelectEdge, plateSelectButton);
	set4 (plateSelectDelta, 1, (unlocked && spiked1 (plateSelectEdge)), 0);
	set4 (plateSelectNr, ((Int) (plateSelectNr + plateSelectDelta) % (Int) 4), power, 0);
	trigger2 (upEdge, upButton);
	trigger2 (downEdge, downButton);

	// Part: Cooking alarm

	trigger2 (alarmSelectEdge, (power && alarmSelectButton));
	mark3 (alarmSelected, (!alarmSelected), (unlocked && spiked1 (alarmSelectEdge)));
	reset2 (alarmChangeTimer, (!(alarmSelected && (upButton || downButton))));
	set4 (alarmChangeStep, 1, (elapsed1 (alarmChangeTimer) > 0), 0);
	set3 (alarmChangeStep, 10, (elapsed1 (alarmChangeTimer) > 10));
	set3 (alarmChangeStep, 100, (elapsed1 (alarmChangeTimer) > 20));
	set4 (alarmDelta, (-alarmChangeStep), downButton, alarmChangeStep);
	set4 (alarmTime, 0, (power && upButton && downButton), limit3 ((alarmTime + (alarmDelta * period)), 0, 9999));
	latch2 (alarmOn, (elapsed1 (alarmChangeTimer) > 0));
	reset2 (alarmTimer, ((!alarmOn) || (elapsed1 (alarmChangeTimer) > 0)));
	trigger2 (alarmEdge, ((elapsed1 (alarmTimer) > alarmTime) || (childLock && (powerButton || plateSelectButton || alarmSelectButton || plateSelectButton || upButton || downButton))));
	unlatch2 (alarmOn, (spiked1 (alarmEdge) || (alarmTime == 0)));
	set2 (alarmTimeLeft, max2 ((alarmTime - elapsed1 (alarmTimer)), 0));

	// Part: Cooking plates

	mark2 (plate0Selected, (plateSelectNr == 0));
	mark2 (plate1Selected, (plateSelectNr == 1));
	mark2 (plate2Selected, (plateSelectNr == 2));
	mark2 (plate3Selected, (plateSelectNr == 3));
	mark2 (tempChange, (unlocked && (!alarmSelected) && (spiked1 (upEdge) || spiked1 (downEdge))));
	set4 (tempDelta, (-1), ((!alarmSelected) && downButton), 1);
	set3 (plate0Temp, limit3 ((plate0Temp + tempDelta), 0, 9), (tempChange && plate0Selected));
	set3 (plate1Temp, limit3 ((plate1Temp + tempDelta), 0, 9), (tempChange && plate1Selected));
	set3 (plate2Temp, limit3 ((plate2Temp + tempDelta), 0, 9), (tempChange && plate2Selected));
	set3 (plate3Temp, limit3 ((plate3Temp + tempDelta), 0, 9), (tempChange && plate3Selected));

	// Part: Buzzer tone generation and pitch bend

	latch2 (buzzerOn, spiked1 (alarmEdge));
	reset2 (buzzerOnTimer, (!buzzerOn));
	unlatch2 (buzzerOn, (elapsed1 (buzzerOnTimer) > buzzerOnTime));
	reset2 (buzzerPitchTimer, (elapsed1 (buzzerPitchTimer) > 3));
	set2 (buzzerFreq, (buzzerBaseFreq * (1 + elapsed1 (buzzerPitchTimer))));
	reset2 (buzzerWaveTimer, (elapsed1 (buzzerWaveTimer) > (0.5 / buzzerFreq)));
	trigger2 (buzzerEdge, (elapsed1 (buzzerWaveTimer) == 0));
	mark3 (buzzer, (!buzzer), (buzzerOn && spiked1 (buzzerEdge)));

	// Part: Numerical display

	set2 (digitIndex, ((Int) (digitIndex + 1) % (Int) 4));
	set3 (plateDigitValue, plate0Temp, (digitIndex == 3));
	set3 (plateDigitValue, plate1Temp, (digitIndex == 2));
	set3 (plateDigitValue, plate2Temp, (digitIndex == 1));
	set3 (plateDigitValue, plate3Temp, (digitIndex == 0));
	set2 (alarmDigitValue, digit2 (alarmTimeLeft, digitIndex));
	set4 (digitValue, alarmDigitValue, alarmSelected, plateDigitValue);
	mark3 (digitDot, plate0Selected, (digitIndex == 3));
	mark3 (digitDot, plate1Selected, (digitIndex == 2));
	mark3 (digitDot, plate2Selected, (digitIndex == 1));
	mark3 (digitDot, plate3Selected, (digitIndex == 0));
	mark3 (digitDot, True, childLock);
	mark3 (digitDot, False, alarmSelected);

	// Part: Sweep time measurement

	set3 (sweepMin, period, (period < sweepMin));
	set3 (sweepMax, period, (period > sweepMax));
	reset2 (sweepWatch, (elapsed1 (sweepWatch) > 2));
	set3 (sweepMin, 1000, (!elapsed1 (sweepWatch)));
	set3 (sweepMax, 0, (!elapsed1 (sweepWatch)));

    // ______ System ______

    update ();
}



// ======================== END OF GENERATED CODE ========================

 

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
