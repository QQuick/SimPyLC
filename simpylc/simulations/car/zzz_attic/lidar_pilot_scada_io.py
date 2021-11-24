# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
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

import multiprocessing.shared_memory as sm
import lidar_pilot_base as lb
import scada_common as sc

class LidarPilotScadaIo (lb.LidarPilotBase):
    def __init__ (self):
        self.scadaList = sm.ShareableList (sc.listValues, name = sc.listName)
        super () .__init__ ()
        
    def input (self):   # Input from scada system
        if self.scadaList [sc.enableDriveIndex]:
            self.driveEnabled = True
        elif self.scadaList [sc.disableDriveIndex]:
            self.driveEnabled = False
    
    def output (self):  # Output to scada system
        self.scadaList [sc.driveEnabledIndex] = self.driveEnabled
        self.scadaList [sc.steeringAngleIndex] = self.steeringAngle
        self.scadaList [sc.targetVelocityIndex] = self.targetVelocity
