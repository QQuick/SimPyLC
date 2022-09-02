import almanac as an

class Deckhand:
    def __init__ (self, crew):
        self.crew = crew

    def work (self, sweep):
        # Make connection
        # In a loop, call input, sweep, output and sleep in that order

    def input (self):
        # Receive sensor data from ship

    def output (self):
        # Send actuator data to ship

    def getCurrentLocation (self):
        # Read out GPS data
        # ...
        # Convert to signed lattitude, longitude (see comment in almanac)
        # ...
        return lattitude, longitude

    def getCourseAngle (self):
        # Read out compass
        # ...
        # Convert to signed angle between -180 and 180 degrees, north == 0, east == 90, west == -90
        # ...
        return courseAngle

    def getVaneAngle (self):
        # Read out wind vane
        # ...
        # Convert to signed angle between -180 and 180 degrees, stern == 0, counter clockwise == 90, clockwise == -90
        # ...
        return vaneAngle

    def setRudderAngle (self, courseAngle):
        # Convert from signed angle between -180 and 180 degrees, stern == 0, counter clockwise == 90, clockwise == -90
        # ...
        # Write to rudder servo
        # ...

    def setSailAngle (self, sailAngle):
        # Convert from signed angle between -180 and 180 degrees, stern == 0, counter clockwise == 90, clockwise == -90
        # ...
        # Write to sheet winch, to sail servo or to the all encompassing nothing
        # ...

    def holdPosition (self):
        # Let sail direction freely go along with the wind direction
        # ...
        # Write to sheet winch, to sail servo or to the all encompassing nothing
        # ...

