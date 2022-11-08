print ('N.B. The .kml file must have been saved in the "decimal degrees" mode!')
filePrename = input ('Prename of .kml file, i.e. without extension: ')
kmlFile = open (filePrename + '.kml')

while True:
    line = kmlFile.readline ()
    if '<coordinates>' in line:
        break

waypointsFile = open (filePrename + '.waypoints', 'w')

while True:
    line = kmlFile.readline ()
    if '</coordinates>' in line:
        break

    triplets = [item.split (',') for item in line.split ()]
    waypoints = [(lattitude, longitude) for longitude, lattitude, height in triplets]

    for waypoint in waypoints:
        print (waypoint [0], waypoint [1], file = waypointsFile)

print (f'Conversion from {filePrename}.kml to {filePrename}.waypoints done.')
