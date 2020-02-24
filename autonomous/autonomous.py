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
        if reset:
            self.drivetrain.reset_distance()
        if distance > 0:
            if not slow:
                self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED,
                                           config.Robot.DRIVE_SPEED)
            else:
                self.drivetrain.set_speeds(config.Robot.DRIVE_SLOW_SPEED,
                                           config.Robot.DRIVE_SLOW_SPEED)
            return self.drivetrain.get_distance() > distance
        if not slow:
            self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED,
                                       -config.Robot.DRIVE_SPEED)
        else:
            self.drivetrain.set_speeds(-config.Robot.DRIVE_SLOW_SPEED,
                                       -config.Robot.DRIVE_SLOW_SPEED)
        return self.drivetrain.get_distance() < distance

    def turn(self, reset: bool, angle: float):
        if reset:
            self.navx.reset()
        if angle > 0:
            self.drivetrain.set_speeds(config.Robot.DRIVE_TURN_SPEED,
                                       -config.Robot.DRIVE_TURN_SPEED)
            return self.navx.getAngle() % 360 > angle
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED,
                                   config.Robot.DRIVE_TURN_SPEED)
        return self.navx.getAngle() % 360 < angle
    def shoot(self, reset: bool):
        if reset:
            self.drivetrain.set_speeds(0,0)
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)
