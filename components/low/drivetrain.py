import ctre


class Drivetrain:
    def __init__(self, front_left: ctre.WPI_TalonSRX,
                 front_right: ctre.WPI_TalonSRX, back_left: ctre.WPI_TalonSRX,
                 back_right: ctre.WPI_TalonSRX):
        self.front_left = front_left
        self.front_right = front_right
        self.back_left = back_left
        self.back_right = back_right
        self.speed_left = 0
        self.speed_right = 0

    def set_speeds_from_joystick(self, x, y, twist):
        speed_left = (-y + (x if x > 0 else 0) + twist)
        speed_right = (-y - (x if x < 0 else 0) - twist)
        # Normalization
        speed_max = max(abs(speed_left), abs(speed_right))
        if speed_max > 1:
            speed_left /= speed_max
            speed_right /= speed_max
        # Set speeds
        self.set_speeds(speed_left, speed_right)

    def set_speeds(self, speed_left, speed_right):
        self.speed_left = speed_left
        self.speed_right = speed_right
        self.front_left.set(self.speed_left)
        self.front_right.set(self.speed_right)
        self.back_left.set(self.speed_left)
        self.back_right.set(self.speed_right)

    def get_speeds(self):
        return (self.speed_left, self.speed_right)
