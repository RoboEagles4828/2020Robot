from navx import AHRS

import config
from components.low.drivetrain import Drivetrain


class Autonomous:
    def __init__(self, drivetrain: Drivetrain, navx: AHRS):
        self.drivetrain = drivetrain
        self.navx = navx

    def drive(self, reset: bool, distance: float, slow=False):
        if reset:
            self.drivetrain.reset_distance()
        if distance > 0:
            if not slow:
                self.drivetrain.set_speeds(config.Autonomous.DRIVE_SPEED,
                                           config.Autonomous.DRIVE_SPEED)
            else:
                self.drivetrain.set_speeds(config.Autonomous.DRIVE_SLOW_SPEED,
                                           config.Autonomous.DRIVE_SLOW_SPEED)
            return self.drivetrain.get_distance() > distance
        if not slow:
            self.drivetrain.set_speeds(-config.Autonomous.DRIVE_SPEED,
                                       -config.Autonomous.DRIVE_SPEED)
        else:
            self.drivetrain.set_speeds(-config.Autonomous.DRIVE_SLOW_SPEED,
                                       -config.Autonomous.DRIVE_SLOW_SPEED)
        return self.drivetrain.get_distance() < distance

    def turn(self, reset: bool, angle: float):
        if reset:
            self.navx.reset()
        if angle > 0:
            self.drivetrain.set_speeds(config.Autonomous.DRIVE_TURN_SPEED,
                                       -config.Autonomous.DRIVE_TURN_SPEED)
            return self.navx.getAngle() % 360 > angle
        self.drivetrain.set_speeds(-config.Autonomous.DRIVE_TURN_SPEED,
                                   config.Autonomous.DRIVE_TURN_SPEED)
        return self.navx.getAngle() % 360 < angle
