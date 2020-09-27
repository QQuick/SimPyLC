class KeyboardPilot:
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

        self.targetVelocityStep = self.world.control.targetVelocityStep
        self.steeringAngleStep = self.world.control.steeringAngleStep

    def sweep (self):
        if self.upKey:
            self.targetVelocityStep += 1
            print ('Target velocity step: ', self.targetVelocityStep)
        elif self.downKey:
            self.targetVelocityStep -= 1
            print ('Target velocity step: ', self.targetVelocityStep)
        elif self.leftKey:
            self.steeringAngleStep += 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.rightKey:
            self.steeringAngleStep -= 1
            print ('Steering angle step: ', self.steeringAngleStep)
        
    def writeOutputs (self):
        self.world.control.targetVelocityStep.set (self.targetVelocityStep)
        self.world.control.steeringAngleStep.set (self.steeringAngleStep)
        
