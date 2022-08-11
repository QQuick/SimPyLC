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
Removing this comment ends your license.
'''

import almanac as an

class Captain:
    def __init__ (self, crew):
        self.crew = crew

    def navigate (self):
        self.waypoints = an.getWaypoints ()  # To be replaced by dynamic waypoint adaptation, based on e.g. weather data and current boat position
        self.crew.helmsman.sail ()
