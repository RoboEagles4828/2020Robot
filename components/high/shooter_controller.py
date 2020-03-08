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

    def get_speed_left(self):
        return self.speed_left

    def get_speed_right(self):
        return self.speed_right

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def execute(self):
        if self.enabled:
            if self.velocity != 0:
                if self.speed_left == 0:
                    self.speed_left = self.velocity * config.ShooterController.F_LEFT
                if self.speed_right == 0:
                    self.speed_right = self.velocity * config.ShooterController.F_RIGHT
                self.speed_left += self.shooter_left_controller.calculate(
                    self.shooter.get_shooter_left_velocity(), self.velocity)
                self.speed_right += self.shooter_right_controller.calculate(
                    self.shooter.get_shooter_right_velocity(), self.velocity)
                if abs(self.speed_left) > 1:
                    self.speed_left = self.speed_left / abs(self.speed_left)
                if abs(self.speed_right) > 1:
                    self.speed_right = self.speed_right / abs(self.speed_right)
            else:
                self.speed_left = 0
                self.speed_right = 0
            self.shooter.set_shooter_speed_left(self.speed_left)
            self.shooter.set_shooter_speed_right(self.speed_right)
