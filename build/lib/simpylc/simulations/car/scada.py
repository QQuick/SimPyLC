import multiprocessing.shared_memory as sm
import time as tm

import scada_common as sc

scadaList = sm.ShareableList (name = sc.listName)

while True:
    print (f'Drive enabled: {scadaList [sc.driveEnabledIndex] : 1d}   Steering angle: {scadaList [sc.steeringAngleIndex] : 7.2f}   Target velocity: {scadaList [sc.targetVelocityIndex] : 7.2f}')
    tm.sleep (0.5)
