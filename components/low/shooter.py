"""Shooter module"""
import ctre
import wpilib

import config


class Shooter:
    """Shooter class"""
    def __init__(self, intake: ctre.WPI_TalonSRX, conveyor: ctre.WPI_VictorSPX,
                 conveyor_prox_front: wpilib.DigitalInput,
                 conveyor_prox_back: wpilib.DigitalInput,
                 shooter_left: ctre.WPI_TalonSRX,
                 shooter_right: ctre.WPI_TalonSRX,
                 shooter_piston_0: wpilib.Solenoid,
                 shooter_piston_1: wpilib.Solenoid):
        self.intake = intake
        self.conveyor = conveyor
        self.conveyor_prox_front = conveyor_prox_front
        self.conveyor_prox_back = conveyor_prox_back
        self.shooter_left = shooter_left
        self.shooter_right = shooter_right
        self.shooter_piston_0 = shooter_piston_0
        self.shooter_piston_1 = shooter_piston_1
        self.intake_speed = 0
        self.conveyor_status = False
        self.conveyor_prox_front_status = False
        self.conveyor_prox_back_status = False
        self.shooter_speed = 0
        self.shooter_status = False
        self.timer = wpilib.Timer()

    def set_intake_speed(self, speed):
        self.intake_speed = speed
        if speed != 0:
            self.set_shooter(True)

    def get_intake_speed(self):
        return self.intake_speed

    def set_conveyor(self, status):
        self.conveyor_status = status

    def get_conveyor_prox_front(self):
        return self.conveyor_prox_front_status

    def get_conveyor_prox_back(self):
        return self.conveyor_prox_back_status

    def set_shooter_speed(self, speed):
        self.shooter_speed = speed

    def set_shooter(self, status):
        self.shooter_status = status

    def get_shooter(self):
        return self.shooter_status

    def execute(self):
        self.intake.set(self.intake_speed)
        self.conveyor_prox_front_status = self.conveyor_prox_front.get()
        self.conveyor_prox_back_status = not self.conveyor_prox_back.get()
        if self.shooter_speed != 0:
            if self.timer.hasElapsed(1.0):
                self.conveyor.set(config.Shooter.CONVEYOR_SHOOT_SPEED)
            self.timer.start()
        elif (self.get_conveyor_prox_front()
              and not self.get_conveyor_prox_back()) or self.conveyor_status:
            self.timer.stop()
            self.timer.reset()
            self.conveyor.set(config.Shooter.CONVEYOR_INTAKE_SPEED)
        else:
            self.timer.stop()
            self.timer.reset()
            self.conveyor.set(0)
        self.shooter_left.set(self.shooter_speed)
        self.shooter_right.set(-self.shooter_speed)
        self.shooter_piston_0.set(self.shooter_status)
        self.shooter_piston_1.set(self.shooter_status)
