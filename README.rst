=== ANNOUNCEMENT: You can now use the SimPyLC `FORUM <http://simpylc.freeforums.net/>`_ to share knowledge and ask questions about SimPyLC. ===

.. figure:: http://www.qquick.org/simpylc/robotvisualisation.jpg
	:alt: Screenshot of SimPyLC
	
	**Simulate your PLC controls and controlled systems to save lots of commissioning time**

PLC?

Real world industrial control systems DO NOT consist of a bunch of communicating sequential processes. Semaphores, threads and priority jugling are far too error prone to control anything else but a model railway. Most control systems are surprisingly simple, consisting of only one program loop that nevertheless seems to do many things in parallel and with reliable timing. Such a control system is called a PLC (Programmable Logic Controller) and all major industries rely on it. PLC's control trains, cranes, ships and your washing machine.
		
What SimPyLC is not:

SimPyLC does not attempt to mimic any particular PLC instruction set or graphical representation like ladder logic or graphcet. There are enough tools that do. Anyone with experience in the field and an IT background knows that such archaic, bulky, hard to edit representations get in the way of clear thinking. By the way, graphcet is stateful per definition, which is the absolute enemy of safety. Though its bigger brother written in C++ according to exactly the same principles has been reliably controlling container cranes, grab unloaders and production lines for more than 20 years now, SimPyLC is FUNDAMENTALLY UNSUITABLE for controlling real world systems and should never be used as a definitive validation of anything. You're only allowed to use SimPyLC under the conditions specified in the qQuickLicence that's part of the distribution.

What it is:

SimPyLC functionally behaves like a PLC or a set of interconnected PLC's and controlled systems. It is a very powerful tool to gain insight in the behaviour of real time controls and controlled systems. It allows you to force values, to freeze time, to draw timing charts and to visualize your system. This is all done in a very simple and straightforward way. But make no mistake, simulating systems in this way has a track record of reducing months of commissioning time to mere days. SimPyLC is Form Follows Function at its best, it does what it has to do in a robust no-nonsense way. Its sourcecode is tiny and fully open to understanding. The accompanying `SimPyLCHowTo <http://www.qquick.org/simpylchowto>`_ condenses decenia of practical experience in control systems in a few clear design rules that can save you lots of trouble and prevent accidents. In addition to this SimPyLC can generate C code for the Arduino processor boards.

.. figure:: http://www.qquick.org/simpylc/arduinodue.jpg
	:alt: Picture of Arduino Due
	
	**SimPyLC is able to generate C code for Arduino processor boards, making Arduino development MUCH easier**

So:

Are you looking for impressive graphics: Look elsewhere. Do you want to gain invaluable insight in real time behaviour of controls and control systems with minimal effort: Use SimPyLC, curse at its anachronistic simplicity and grow to love it more and more.

What's new:

- Comments in code of SimPyLC/scene.py adapted to clarify different purpose of axis and pivot, and of passing angle to __init__ versus passing it to __call__
- Spaces rather than tabs are now used in the sourcecode.
- Adapted for Python 3.5 (SimPyLC 2.1.2 is last version running with Python 2.7)
- Development status bumped to production / stable.
- Native.py files replaced by native.cpp files, which are plain C++, hence benefit from syntax highlighting. You'll have to adapt your existing code to this (by merely leaving things out).
- Code now generated in a separate subdirectory to avoid confusion, especially with native.cpp.
- Cooking stove example I/O assignment for Arduino Due and hardware description added.
- Some changes to the visualisation API, parameters to overloaded () operator of Beam and Cylinder now have to be named. This is not backwards compatible, you'll have to add parameter names to visualisations of your old projects. Look at what has changed in the oneArmedRobot simulation, module visualisation.py, to understand what this is about. Using named parameters gives more flexibility in changing other things than angles in your visualisations, e.g. position or color. This is used very modestly in the new arduinoStove example. 

REMARK: All complete Arduino examples were tested on the Arduino Due, since that's the one I own, but they should run on the One with only slight I/O modifications (PWM instead of true analog output, using a shift register if you run short of I/O pins etc.)

Bugs fixed:

- __nonzero__ changed to __bool__, as required by the move from Python 2.7 to Python 3.5. The blinkingLight demo will now work again.
- Sidewalks raised above road in arduinoTrafficLights example.
- Unused circuit group 'Lights' deleted from control in arduinoTrafficLights example.

**Bug reports and feature requests are most welcome and will be taken under serious consideration on a non-committal basis**
		
Requirements for Windows:

1. Install WinPython 3.5, e.g. from https://winpython.github.io
2. (Optional) Copy SimPyLC\\SimPyLC\\QuartzMS.TTF to C:\\Windows\\Fonts
3. (Optional) You can may also add SimPyLC\\SimPyLC to your PYTHONPATH

Requirements for Linux:

1. Install Python 3.5 and PyOpenGL

Usage:

1. Go to directory SimPyLC/simulations/oneArmedRobot
2. Click on world.py or run world.py from the command line

GUI Operation:

- [LEFT CLICK] on a field or [ENTER] gets you into edit mode.
- [LEFT CLICK] or [ENTER] again gets you out of edit mode and into forced mode, values coloured orange are frozen.
- [RIGHT CLICK] or [ESC] gets gets you into released mode, values are thawed again.
- [PGUP] and [PGDN] change the currently viewed control page.

For a test run of oneArmedRobot:

- Enter setpoints in degrees for the joint angles (e.g. torAngSet for the torso of the robot) on the movement control page.
- After that set 'go' to 1 and watch what happens.

If you want to experiment yourself, read `SimPyLCHowTo <http://www.qquick.org/simpylchowto>`_

	.. figure:: http://www.qquick.org/simpylc/robotsimulationsource.jpg
		:alt: A sample SimPyLC program
		
		**Coding is text oriented, enabling simple and fast editing, but functional behaviour resembles circuit logic, with elements like markers, timers, oneshots, latches and registers**

Other packages you might like:

- Lean and mean Python to JavaScript transpiler featuring multiple inheritance https://pypi.python.org/pypi/Transcrypt
- Multi-module Python source code obfuscator https://pypi.python.org/pypi/Opy
- Event driven evaluation nodes https://pypi.python.org/pypi/Eden
- A lightweight Python course taking beginners seriously (under construction): https://pypi.python.org/pypi/LightOn
