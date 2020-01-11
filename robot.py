"""Main robot module"""
import wpilib


class Robot(wpilib.TimedRobot):
    """Main robot class"""
    def robotInit(self):
        """Robot initialization"""
        # Create timer
        self.timer = wpilib.Timer()
        # Create joystick
        self.joystick = wpilib.Joystick(1)

    def autonomousInit(self):
        """Autonomous mode initialization"""

    def autonomousPeriodic(self):
        """Autonomous mode periodic (20ms)"""

    def teleopInit(self):
        """Teleoperated mode initialization"""
        self.timer.reset()
        self.timer.start()

    def teleopPeriodic(self):
        """Teleoperated mode periodic (20ms)"""

    def disabledInit(self):
        """Disabled mode initialization"""

    def disabledPeriodic(self):
        """Disabled mode periodic (20ms)"""


if __name__ == "__main__":
    wpilib.run(Robot)
