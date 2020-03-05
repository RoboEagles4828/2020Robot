from components.low.shooter import Shooter


class ShooterController:
    def __init__(self, shooter: Shooter):
        self.shooter_left_controller = wpilib.controller.PIDController(
            config.Shooter.P_LEFT, config.Shooter.I_LEFT,
            config.Shooter.D_LEFT)
        self.shooter_right_controller = wpilib.controller.PIDController(
            config.Shooter.P_RIGHT, config.Shooter.I_RIGHT,
            config.Shooter.D_RIGHT)
