from navx import AHRS

import config
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class Autonomous:
    def __init__(self, drivetrain: Drivetrain, navx: AHRS, shooter: Shooter):
        self.drivetrain = drivetrain
        self.navx = navx
        self.shooter = shooter

    def drive(self, reset: bool, distance: float, slow=False):
        self.shooter.set_shooter_speed(0)
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
        self.shooter.set_shooter_speed(0)
        if reset:
            self.navx.reset()
        if angle > 0:
            self.drivetrain.set_speeds(
                config.Robot.Drivetrain.DRIVE_TURN_SPEED,
                -config.Robot.Drivetrain.DRIVE_TURN_SPEED)
            return self.navx.getAngle() % 360 > angle
        self.drivetrain.set_speeds(-config.Robot.Drivetrain.DRIVE_TURN_SPEED,
                                   config.Robot.Drivetrain.DRIVE_TURN_SPEED)
        return self.navx.getAngle() % 360 < angle

    def shoot_0(self):
        self.drivetrain.set_speeds(0, 0)
        self.shooter.set_shooter_speed(config.Robot.Shooter.SHOOTER_SPEED_0)

    def shoot_1(self):
        self.drivetrain.set_speeds(0, 0)
        self.shooter.set_shooter_speed(config.Robot.Shooter.SHOOTER_SPEED_1)
