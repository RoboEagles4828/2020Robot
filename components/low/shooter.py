"""Shooter module"""
import ctre
import wpilib


class Shooter:
    """Shooter class"""
    def __init__(
        self, intake: ctre.WPI_TalonSRX, intake_motor: ctre.WPI_VictorSPX,
        conveyor: ctre.VictorSPX, conveyor_prox_front: wpilib.DigitalInput,
        conveyor_prox_back: wpilib.DigitalInput,
        shooter_left: ctre.WPI_TalonSRX, shooter_right: ctre.WPI_TalonSRX,
        shooter_piston_0: wpilib.DoubleSolenoid,
        shooter_piston_1: wpilib.DoubleSolenoid):
        self.intake = intake
        self.intake_motor = intake_motor
        self.conveyor = conveyor
        self.conveyor_prox_front = conveyor_prox_front
        self.conveyor_prox_back = conveyor_prox_back
        self.shooter_left = shooter_left
        self.shooter_right = shooter_right
        self.shooter_piston_0 = shooter_piston_0
        self.shooter_piston_1 = shooter_piston_1
        self.intake_speed = 0
        self.intake_status = True
        self.conveyor_speed = 0
        self.conveyor_prox_front_status = False
        self.conveyor_prox_back_status = False
        self.shooter_speed = 0
        self.shooter_status = False
        self.control_mode = ctre.ControlMode(0)

    def set_intake_speed(self, speed):
        self.intake_speed = speed

    def set_intake(self, status):
        self.intake_status = status

    def set_conveyor_speed(self, speed):
        self.conveyor_speed = speed

    def set_shooter_speed(self, speed):
        self.shooter_speed = speed

    def set_shooter(self, status):
        self.shooter_status = status

    def get_conveyor_prox_front(self):
        return self.conveyor_prox_front_status

    def get_conveyor_prox_back(self):
        return self.conveyor_prox_back_status

    def execute(self):
        if self.intake_status:
            self.intake_motor.set(self.control_mode.PercentOutput, .5)
            self.intake_status = False
        else:
            self.intake_motor.set(self.control_mode.PercentOutput, 0)
        self.intake.set(self.intake_speed)
        self.conveyor.set(self.control_mode.PercentOutput, self.conveyor_speed)
        self.conveyor_prox_front_status = self.conveyor_prox_front.get()
        self.conveyor_prox_back_status = self.conveyor_prox_back.get()
        self.shooter_left.set(self.shooter_speed)
        self.shooter_right.set(-self.shooter_speed)
        if self.shooter_status:
            self.shooter_piston_0.set(wpilib.Solenoid.Value.kForward)
            self.shooter_piston_1.set(wpilib.Solenoid.Value.kForward)
        else:
            self.shooter_piston_0.set(wpilib.Solenoid.Value.kReverse)
            self.shooter_piston_1.set(wpilib.Solenoid.Value.kReverse)
