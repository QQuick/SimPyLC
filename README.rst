=== Use the `SimPyLC forum <http://simpylc.freeforums.net/>`_ to share knowledge and ask questions about SimPyLC. ===

.. figure:: http://www.qquick.org/simpylc/robotvisualisation.jpg
	:alt: Screenshot of SimPyLC
	
	**Simulate your PLC controls and controlled systems to save lots of commissioning time**

PLC?
----

Real world industrial control systems DO NOT consist of a bunch of communicating sequential processes. Semaphores, threads and priority jugling are far too error prone to control anything else but a model railway. Most control systems are surprisingly simple, consisting of only one program loop that nevertheless seems to do many things in parallel and with reliable timing. Such a control system is called a PLC (Programmable Logic Controller) and all major industries rely on it. PLC's control trains, cranes, ships and your washing machine.
		
What SimPyLC is not
-------------------

SimPyLC does not attempt to mimic any particular PLC instruction set or graphical representation like ladder logic or graphcet. There are enough tools that do. Anyone with experience in the field and an IT background knows that such archaic, bulky, hard to edit representations get in the way of clear thinking. By the way, graphcet is stateful per definition, which is the absolute enemy of safety. Though its bigger brother written in C++ according to exactly the same principles has been reliably controlling container cranes, grab unloaders and production lines for more than 20 years now, SimPyLC is FUNDAMENTALLY UNSUITABLE for controlling real world systems and should never be used as a definitive validation of anything. You're only allowed to use SimPyLC under the conditions specified in the qQuickLicence that's part of the distribution.

What it is
----------

SimPyLC functionally behaves like a PLC or a set of interconnected PLC's and controlled systems. It is a very powerful tool to gain insight in the behaviour of real time controls and controlled systems. It allows you to force values, to freeze time, to draw timing charts and to visualize your system. This is all done in a very simple and straightforward way. But make no mistake, simulating systems in this way has a track record of reducing months of commissioning time to mere days. SimPyLC is Form Follows Function at its best, it does what it has to do in a robust no-nonsense way. Its sourcecode is tiny and fully open to understanding. The accompanying document *simpylc_howto* condenses decenia of practical experience in control systems in a few clear design rules that can save you lots of trouble and prevent accidents. In addition to this SimPyLC can generate C code for the Arduino processor boards.

.. figure:: http://www.qquick.org/simpylc/arduinodue.jpg
	:alt: Picture of Arduino Due
	
	**SimPyLC is able to generate C code for Arduino processor boards, making Arduino development MUCH easier**

So
--

Are you looking for impressive graphics: Look elsewhere. Do you want to gain invaluable insight in real time behaviour of controls and control systems with minimal effort: Use SimPyLC, curse at its anachronistic simplicity and grow to love it more and more.

What's new
----------

- Command line tool *splc* made available
- Parameter attitude added to Thing.__call__ to be able to use rotation matrix rather than Euler angles
- Document simpylc_howto updated and renamed to pothole case
- Boolean circuits can now be switched by pressing the mousewheel
- Registers can now be altered by rotating the mousewheel
- Rocket example added with physically correct moment of inertia to demonstrate e.g. precession
- Some parameters added and some renamed to make Thing.__call__ more consistent
- Function tEva added to evaluate 3D tuples
- Quaternion module added to accurately model rotational movement
- Cones and Ellipsoids added
- Optional moving camera added with synchroneous caching for accurate tracking
- Pure Python controls added, just using the simulator to test without actual controlled hardware

*REMARK: All complete Arduino examples were tested on the Arduino Due, since that's the one I own, but they should run on the One with only slight I/O modifications (PWM instead of true analog output, using a shift register if you run short of I/O pins etc.)*

Bugs fixed
----------

- No known bugs currently

**Bug reports and feature requests are most welcome and will be taken under serious consideration on a non-committal basis**
		
Installation
------------

Installation for Windows, Linux and OSX is described in the *sympylc_howto* document.

Usage
-----

1. Go to directory SimPyLC/simulations/oneArmedRobot
2. Click on world.py or run world.py from the command line

GUI Operation
-------------

- [LEFT CLICK] on a field or [ENTER] gets you into edit mode.
- [LEFT CLICK] or [ENTER] again gets you out of edit mode and into forced mode, values coloured orange are frozen.
- [RIGHT CLICK] or [ESC] gets you into released mode, values are thawed again.
- [PGUP] and [PGDN] change the currently viewed control page.
- [WHEEL PRESSED] on a marker field makes it 1, release makes it 0 again, both without freezing it.
- [WHEEL ROTATION] changes the value of a register field, without freezing it.


For a test run of oneArmedRobot
-------------------------------

1. Enter setpoints in degrees for the joint angles (e.g. torAngSet for the torso of the robot) on the movement control page.
2. After that set 'go' to 1 and watch what happens.

If you want to experiment yourself, read `SimPyLCHowTo <http://www.qquick.org/simpylchowto>`_

	.. figure:: http://www.qquick.org/simpylc/robotsimulationsource.jpg
		:alt: A sample SimPyLC program
		
		**Coding is text oriented, enabling simple and fast editing, but functional behaviour resembles circuit logic, with elements like markers, timers, oneshots, latches and registers**

Other packages you might like
-----------------------------

- Lean and mean Python to JavaScript transpiler featuring multiple inheritance https://pypi.python.org/pypi/Transcrypt
- Multi-module Python source code obfuscator https://pypi.python.org/pypi/Opy
- Event driven evaluation nodes https://pypi.python.org/pypi/Eden
- A lightweight Python course taking beginners seriously (under construction): https://pypi.python.org/pypi/LightOn
