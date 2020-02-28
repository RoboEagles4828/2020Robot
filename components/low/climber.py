"""Climber module"""
import ctre


class Climber:
    """Climber class"""
    def __init__(self, climber_left: ctre.WPI_TalonSRX,
                 climber_right: ctre.WPI_TalonSRX,
                 winch_left_front: ctre.WPI_VictorSPX,
                 winch_left_back: ctre.WPI_VictorSPX,
                 winch_right_front: ctre.WPI_VictorSPX,
                 winch_right_back: ctre.WPI_VictorSPX):
        self.climber_left = climber_left
        self.climber_right = climber_right
        self.winch_left_front = winch_left_front
        self.winch_left_back = winch_left_back
        self.winch_right_front = winch_right_front
        self.winch_right_back = winch_right_back
        self.climber_left_speed = 0
        self.climber_right_speed = 0
        self.winch_left_front_speed = 0
        self.winch_left_back_speed = 0
        self.winch_right_front_speed = 0
        self.winch_right_back_speed = 0

    def set_climber_left_speed(self, speed):
        self.climber_left_speed = speed

    def set_climber_right_speed(self, speed):
        self.climber_right_speed = speed

    def set_winch_left_front_speed(self, speed):
        self.winch_left_front_speed = speed

    def set_winch_left_back_speed(self, speed):
        self.winch_left_back_speed = speed

    def set_winch_right_front_speed(self, speed):
        self.winch_right_front_speed = speed

    def set_winch_right_back_speed(self, speed):
        self.winch_right_back_speed = speed

    def execute(self):
        self.climber_left.set(self.climber_left_speed)
        self.climber_right.set(self.climber_right_speed)
        self.winch_left_front.set(self.winch_left_front_speed)
        self.winch_left_back.set(-self.winch_left_back_speed)
        self.winch_right_front.set(-self.winch_right_front_speed)
        self.winch_right_back.set(self.winch_right_back_speed)
