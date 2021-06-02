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

import argparse as ap
import distutils.dir_util as du
import os
import webbrowser as wb

simulationsSubdirName = 'simulations'
accessoriesSubdirName = 'accessories'
howtoFileName = 'simpylc_howto.pdf'

class CommandArgs :
    def __init__ (self):
        self.argParser = ap.ArgumentParser ()
        self.argParser.add_argument ('-a', '--acc', help = "Copy accessories to current directory", action = 'store_true')
        self.argParser.add_argument ('-d', '--doc', help = "Show documentation in default browser", action = 'store_true')
        self.argParser.add_argument ('-s', '--sim', help = "Copy example simulations to directory", action = 'store_true')
        self.__dict__.update (self.argParser.parse_args () .__dict__)
    
        
commandArgs = CommandArgs ()

simulatorDir = os.path.dirname (os.path.realpath (__file__))
currentDir = os.getcwd ()

if commandArgs.acc:
    du.copy_tree (simulatorDir + '/' + accessoriesSubdirName, currentDir + '/' + accessoriesSubdirName)
elif commandArgs.sim:
    du.copy_tree (simulatorDir + '/' + simulationsSubdirName, currentDir + '/' + simulationsSubdirName)
elif commandArgs.doc:
    wb.open (simulatorDir + '/' + howtoFileName)
else:
    commandArgs.argParser.print_help ()
   
