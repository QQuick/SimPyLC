# ====== Legal notices
#
# Copyright (C) 2013  - 2020 GEATEC engineering
#
# This program is free software./
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

import time as tm

class Timer:
    def __init__ (self):
        self.time = tm.time ()
       
    def tick (self):
        self._oldTime = self.time
        self.time = tm.time ()
        self.deltaTime = self.time - self._oldTime
        
