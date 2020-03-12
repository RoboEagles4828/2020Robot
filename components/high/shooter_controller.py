import wpilib.controller

import config
from components.low.shooter import Shooter


class ShooterController:
    def __init__(self, shooter: Shooter):
        self.shooter = shooter
        self.shooter_left_controller = wpilib.controller.PIDController(
            config.ShooterController.P_LEFT, config.ShooterController.I_LEFT,
            config.ShooterController.D_LEFT)
        self.shooter_right_controller = wpilib.controller.PIDController(
            config.ShooterController.P_RIGHT, config.ShooterController.I_RIGHT,
            config.ShooterController.D_RIGHT)
        self.speed_left = 0
        self.speed_right = 0
        self.velocity = 0
        self.enabled = False

    def set_velocity(self, velocity):
        self.velocity = velocity

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def execute(self):
        if self.enabled:
            self.speed_left = config.ShooterController.F_LEFT * self.velocity + (
                self.shooter_left_controller.calculate(
                    self.shooter.get_shooter_velocity_left(), self.velocity))
            self.speed_right = config.ShooterController.F_RIGHT * self.velocity + (
                self.shooter_right_controller.calculate(
                    self.shooter.get_shooter_velocity_right(), self.velocity))
            self.speed_left = max(0, min(1, self.speed_left))
            self.speed_right = max(0, min(1, self.speed_right))
            self.shooter.set_shooter_speed_left(self.speed_left)
            self.shooter.set_shooter_speed_right(self.speed_right)
