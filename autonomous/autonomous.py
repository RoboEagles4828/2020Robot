from navx import AHRS
from networktables import NetworkTable

import config
from components.low.drivetrain import Drivetrain
from components.high.shooter_controller import ShooterController


class Autonomous:
    def __init__(self, drivetrain: Drivetrain, navx: AHRS,
                 shooter_controller: ShooterController, nt_pi: NetworkTable):
        self.drivetrain = drivetrain
        self.navx = navx
        self.shooter_controller = shooter_controller
        self.nt_pi = nt_pi

    def drive(self, reset: bool, distance: float, slow=False):
        self.shooter_controller.set_velocity(0)
        if reset:
            self.drivetrain.reset_distance()
        if distance > 0:
            if not slow:
                self.drivetrain.set_speeds(config.Robot.Drivetrain.DRIVE_SPEED,
                                           config.Robot.Drivetrain.DRIVE_SPEED)
            else:
                self.drivetrain.set_speeds(
                    config.Robot.Drivetrain.DRIVE_SLOW_SPEED,
                    config.Robot.Drivetrain.DRIVE_SLOW_SPEED)
            return self.drivetrain.get_distance() > distance
        if not slow:
            self.drivetrain.set_speeds(-config.Robot.Drivetrain.DRIVE_SPEED,
                                       -config.Robot.Drivetrain.DRIVE_SPEED)
        else:
            self.drivetrain.set_speeds(
                -config.Robot.Drivetrain.DRIVE_SLOW_SPEED,
                -config.Robot.Drivetrain.DRIVE_SLOW_SPEED)
        return self.drivetrain.get_distance() < distance

    def turn(self, reset: bool, angle: float):
        self.shooter_controller.set_velocity(0)
        if reset:
            self.navx.reset()
        if angle > 0:
            self.drivetrain.set_speeds(
                config.Robot.Drivetrain.DRIVE_TURN_SPEED,
                -config.Robot.Drivetrain.DRIVE_TURN_SPEED)
            return self.navx.getAngle() > angle
        self.drivetrain.set_speeds(-config.Robot.Drivetrain.DRIVE_TURN_SPEED,
                                   config.Robot.Drivetrain.DRIVE_TURN_SPEED)
        return self.navx.getAngle() < angle

    def shoot_0(self):
        self.drivetrain.set_speeds(0, 0)
        self.shooter_controller.set_velocity(
            config.Robot.ShooterController.SHOOTER_VELOCITY_0)

    def shoot_1(self):
        self.drivetrain.set_speeds(0, 0)
        self.shooter_controller.set_velocity(
            config.Robot.ShooterController.SHOOTER_VELOCITY_1)

    def vision(self):
        value = self.nt_pi.getNumber("value", 0) * config.Robot.VISION_RATIO
        if abs(value) < config.Robot.VISION_MIN_SPEED:
            value = value / abs(value) * config.Robot.VISION_MIN_SPEED
        if abs(value) < config.Robot.VISION_DEADZONE:
            value = 0
        self.drivetrain.set_speeds(value, -value)
