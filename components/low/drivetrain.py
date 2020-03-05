"""Drivetrain module"""
import ctre
import config


class Drivetrain:
    """Drivetrain class"""
    def __init__(self, left_0: ctre.WPI_TalonFX, left_1: ctre.WPI_TalonFX,
                 right_0: ctre.WPI_TalonFX, right_1: ctre.WPI_TalonFX):
        self.left_0 = left_0
        self.left_1 = left_1
        self.right_0 = right_0
        self.right_1 = right_1
        self.speed_left = 0
        self.speed_right = 0
        self.raw_distance_left = 0
        self.reset_raw_distance_left = False
        self.raw_distance_right = 0
        self.reset_raw_distance_right = False

    def set_speeds(self, speed_left: float, speed_right: float) -> None:
        """
        Sets the left and right speeds

        :param speed_left: The left speed
        :param speed_right: The right speed
        """
        self.speed_left = speed_left
        self.speed_right = speed_right

    def get_speeds(self) -> tuple:
        """
        Gets the left and right speeds

        :returns: A tuple containing the left speed and the right speed
        """
        return (self.speed_left, self.speed_right)

    def set_speeds_joystick(self, x: float, y: float, twist: float) -> None:
        """
        Sets the left and right speeds from joystick inputs

        :param x: The x value of the joystick
        :param y: The y value of the joystick
        :param twist: The twist value of the joystick
        """
        speed_left = (y + (x if x > 0 else 0) + twist)
        speed_right = (y - (x if x < 0 else 0) - twist)
        # Normalization
        speed_max = max(abs(speed_left), abs(speed_right))
        if speed_max > 1:
            speed_left /= speed_max
            speed_right /= speed_max
        # Set speeds
        self.set_speeds(speed_left, speed_right)

    def get_raw_distance_left(self):
        return self.raw_distance_left

    def get_distance_left(self):
        return self.get_raw_distance_left(
        ) * config.Drivetrain.ENCODER_RATIO_LEFT

    def reset_distance_left(self):
        self.reset_raw_distance_left = True

    def get_raw_distance_right(self):
        return self.raw_distance_right

    def get_distance_right(self):
        return self.get_raw_distance_right(
        ) * config.Drivetrain.ENCODER_RATIO_RIGHT

    def reset_distance_right(self):
        self.reset_raw_distance_right = True

    def get_raw_distance(self):
        return self.get_raw_distance_left()

    def get_distance(self):
        return self.get_distance_left()

    def reset_distance(self):
        self.reset_distance_left()

    def execute(self):
        self.left_0.set(self.speed_left)
        self.left_1.set(self.speed_left)
        self.right_0.set(-self.speed_right)
        self.right_1.set(-self.speed_right)
        if self.reset_raw_distance_left:
            self.left_0.setSelectedSensorPosition(0)
            self.reset_raw_distance_left = False
        self.raw_distance_left = self.left_0.getSelectedSensorPosition()
        if self.reset_raw_distance_right:
            self.right_0.setSelectedSensorPosition(0)
            self.reset_raw_distance_right = False
        self.raw_distance_right = self.right_0.getSelectedSensorPosition()
