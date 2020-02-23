"""Climber module"""
import ctre


class Climber:
    """Climber class"""
    def __init__(self, climber_0: ctre.WPI_TalonSRX,
                 climber_1: ctre.WPI_TalonSRX, winch_0_0: ctre.WPI_TalonSRX,
                 winch_0_1: ctre.WPI_VictorSPX, winch_1_0: ctre.WPI_TalonSRX,
                 winch_1_1: ctre.WPI_VictorSPX):
        self.climber_0 = climber_0
        self.climber_1 = climber_1
        self.winch_0_0 = winch_0_0
        self.winch_0_1 = winch_0_1
        self.winch_1_0 = winch_1_0
        self.winch_1_1 = winch_1_1
        self.climber_speed = 0
        self.winch_speed = 0

    def set_climber_speed(self, speed):
        self.climber_speed = speed

    def set_winch_speed(self, speed):
        self.winch_speed = speed

    def execute(self):
        self.climber_0.set(self.climber_speed)
        self.climber_1.set(self.climber_speed)
        self.winch_0_0.set(self.winch_speed)
        self.winch_0_1.set(-self.winch_speed)
        self.winch_1_0.set(self.winch_speed)
        self.winch_1_1.set(-self.winch_speed)
