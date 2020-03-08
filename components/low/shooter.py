"""Shooter module"""
import ctre
import wpilib

import config


class Shooter:
    """Shooter class"""
    def __init__(self, intake: ctre.WPI_TalonSRX, conveyor: ctre.WPI_VictorSPX,
                 conveyor_prox_front_0: wpilib.DigitalInput,
                 conveyor_prox_front_1: wpilib.DigitalInput,
                 conveyor_prox_back: wpilib.DigitalInput,
                 shooter_left: ctre.WPI_TalonSRX,
                 shooter_right: ctre.WPI_TalonSRX,
                 shooter_piston_0: wpilib.Solenoid,
                 shooter_piston_1: wpilib.Solenoid):
        self.intake = intake
        self.conveyor = conveyor
        self.conveyor_prox_front_0 = conveyor_prox_front_0
        self.conveyor_prox_front_1 = conveyor_prox_front_1
        self.conveyor_prox_back = conveyor_prox_back
        self.shooter_left = shooter_left
        self.shooter_right = shooter_right
        self.shooter_piston_0 = shooter_piston_0
        self.shooter_piston_1 = shooter_piston_1
        self.intake_speed = 0
        self.conveyor_status = False
        self.conveyor_prox_front_0_status = False
        self.conveyor_prox_front_1_status = False
        self.conveyor_prox_back_status = False
        self.shooter_speed_left = 0
        self.shooter_speed_right = 0
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

    def get_conveyor_prox_front_0(self):
        return self.conveyor_prox_front_0_status

    def get_conveyor_prox_front_1(self):
        return self.conveyor_prox_front_1_status

    def get_conveyor_prox_back(self):
        return self.conveyor_prox_back_status

    def set_shooter_speed_left(self, speed):
        self.shooter_speed_left = speed

    def set_shooter_speed_right(self, speed):
        self.shooter_speed_right = speed

    def set_shooter_speed(self, speed):
        self.shooter_speed_left = speed
        self.shooter_speed_right = speed

    def get_shooter_left_velocity(self):
        return self.shooter_left.getSelectedSensorVelocity() / -4096

    def get_shooter_right_velocity(self):
        return self.shooter_right.getSelectedSensorVelocity() / 4096

    def set_shooter(self, status):
        self.shooter_status = status

    def get_shooter(self):
        return self.shooter_status

    def execute(self):
        self.intake.set(self.intake_speed)
        self.conveyor_prox_front_0_status = self.conveyor_prox_front_0.get()
        self.conveyor_prox_front_1_status = self.conveyor_prox_front_1.get()
        self.conveyor_prox_back_status = not self.conveyor_prox_back.get()
        if self.shooter_speed_left != 0 or self.shooter_speed_right != 0:
            if self.timer.hasElapsed(0.5):
                self.conveyor.set(config.Shooter.CONVEYOR_SHOOT_SPEED)
            self.timer.start()
        elif ((self.get_conveyor_prox_front_0()
               or self.get_conveyor_prox_front_1())
              and not self.get_conveyor_prox_back()) or self.conveyor_status:
            self.timer.stop()
            self.timer.reset()
            self.conveyor.set(config.Shooter.CONVEYOR_INTAKE_SPEED)
        else:
            self.timer.stop()
            self.timer.reset()
            self.conveyor.set(0)
        self.shooter_left.set(self.shooter_speed_left)
        self.shooter_right.set(-self.shooter_speed_right)
        self.shooter_piston_0.set(self.shooter_status)
        self.shooter_piston_1.set(self.shooter_status)
