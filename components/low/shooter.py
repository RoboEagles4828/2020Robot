import ctre
import wpilib

class Shooter:
    #Setup Shooter Parts
    #Shooter still needs prox sensor variable
    def __init__(self, intake_motor: ctre.WPI_TalonSRX, intake_piston: wpilib.DoubleSolenoid,
                 conveyor_motor: ctre.WPI_TalonSRX, left_shooter: ctre.WPI_TalonSRX, 
                 right_shooter: ctre.WPI_TalonSRX, shooter_piston: wpilib.DoubleSolenoid):
        self.intake_motor = intake_motor
        self.intake_piston = intake_piston
        self.conveyor_motor = conveyor_motor
        self.left_shooter = left_shooter
        self.right_shooter = right_shooter
        self.shooter_piston = shooter_piston
    def turn_on_intake(self):
        self.intake_motor.set(1)
    def turn_on_shooter(self):
        self.conveyor_motor.set(1)
        self.left_shooter.set(1)
        self.right_shooter.set(1)
    #def shooter_angle(self, high_low):