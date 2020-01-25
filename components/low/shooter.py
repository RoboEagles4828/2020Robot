import ctre
import wpilib

class Shooter:
    #Setup Shooter Parts
    #Shooter still needs prox sensor variable
    def __init__(self, intake_motor: ctre.WPI_TalonSRX, intake_piston: wpilib.DoubleSolenoid,
                 conveyor_motor: ctre.WPI_TalonSRX, left_shooter: ctre.WPI_TalonSRX, 
                 right_shooter: ctre.WPI_TalonSRX, shooter_piston_left: wpilib.DoubleSolenoid,
                 shooter_piston_right: wpilib.DoubleSolenoid, prox_sensor_front: wpilib.DigitalInput,
                 prox_sensor_back: wpilib.DigitalInput):
        self.intake_motor = intake_motor
        self.intake_piston = intake_piston
        self.conveyor_motor = conveyor_motor
        self.left_shooter = left_shooter
        self.right_shooter = right_shooter
        self.shooter_piston_left = shooter_piston_left
        self.shooter_piston_right = shooter_piston_right
        self.prox_sensor_front = prox_sensor_front
        self.prox_sensor_back = prox_sensor_back
        self.intake_speed = 0
        self.conveyor_speed = 0
        self.left_speed = 0
        self.right_speed = 0
        self.shooter_piston_up = False
        self.intake_piston_up = False
    def turn_on_intake(self, intake_speed):
        self.intake_speed = intake_speed
    def turn_on_shooter(self, conveyor_speed, left_speed, right_speed):
        self.conveyor_speed = conveyor_speed
        self.left_speed = left_speed
        self.right_speed = right_speed
    def shooter_angle(self, change_angle):
        if(change_angle):
            self.shooter_piston_up = True
        else:
            self.shooter_piston_up = False
    def intake_angle(self, change_angle):
        if(change_angle):
            self.intake_piston_up = True
        else:
            self.intake_piston_up = False
    def get_front_sensor(self):
        return self.prox_sensor_front.get()
    def get_back_sensor(self):
        return self.prox_sensor_back.get()
    def execute(self):
        self.intake_motor.set(self.intake_speed)
        self.conveyor_motor.set(self.conveyor_speed)
        self.left_shooter.set(self.left_speed)
        self.right_shooter.set(self.right_speed)
        if(self.shooter_piston_up):
            self.shooter_piston_left.set(wpilib.DoubleSolenoid.Value.kForward)
            self.shooter_piston_right.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.shooter_piston_left.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.shooter_piston_right.set(wpilib.DoubleSolenoid.Value.kReverse)
        if(self.intake_piston_up):
            self.intake_piston.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.intake_piston.set(wpilib.DoubleSolenoid.Value.kReverse)
        