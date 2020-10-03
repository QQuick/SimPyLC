import simpylc as sp

class KeyboardPilot:
    def __init__ (self):
        print ('test', 1, 2, 3, 4)
        
        while True:
            self.readInputs ()
            self.sweep ()
            self.writeOutputs ()
            
    def readInputs (self):
        key = sp.getKey ()
        
        self.leftKey = key == 'KEY_LEFT'
        self.rightKey = key == 'KEY_RIGHT'
        self.upKey = key == 'KEY_UP'
        self.downKey = key == 'KEY_DOWN'

        self.targetVelocityStep = sp.world.control.targetVelocityStep
        self.steeringAngleStep = sp.world.control.steeringAngleStep

    def sweep (self):
        if self.leftKey:
            self.steeringAngleStep += 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.rightKey:
            self.steeringAngleStep -= 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.upKey:
            self.targetVelocityStep += 1
            print ('Target velocity step: ', self.targetVelocityStep)
        elif self.downKey:
            self.targetVelocityStep -= 1
            print ('Target velocity step: ', self.targetVelocityStep)
        
    def writeOutputs (self):
        sp.world.control.steeringAngleStep.set (self.steeringAngleStep)
        sp.world.control.targetVelocityStep.set (self.targetVelocityStep)
        
