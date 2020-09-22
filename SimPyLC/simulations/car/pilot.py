class Pilot:
    def __init__ (self):
        while True:
            self.readInputs ()
            self.sweep ()
            self.writeOutputs ()
            
    def readInputs (self):
        key = self.getKey ()
        
        self.upKey = key == 'KEY_UP'
        self.downKey = key == 'KEY_DOWN'
        self.leftKey = key == 'KEY_LEFT'
        self.rightKey = key == 'KEY_RIGHT'

        self.velocityStepper = self.world.control.velocityStepper
        self.steeringStepper = self.world.control.steeringStepper

    def sweep (self):
        if self.upKey:
            self.velocityStepper += 1
            print ('Velocity step: ', self.velocityStepper)
        elif self.downKey:
            self.velocityStepper -= 1
            print ('Velocity step: ', self.velocityStepper)
        elif self.leftKey:
            self.steeringStepper += 1
            print ('Steering step: ', self.steeringStepper)
        elif self.rightKey:
            self.steeringStepper -= 1
            print ('Steering step: ', self.steeringStepper)
        
    def writeOutputs (self):
        self.world.control.velocityStepper.set (self.velocityStepper)
        self.world.control.steeringStepper.set (self.steeringStepper)
        
