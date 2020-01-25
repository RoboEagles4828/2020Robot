"""Main robot module"""
import logging
import wpilib
import ctre

import config
from components.low.analog_input import AnalogInput
from components.low.digital_input import DigitalInput
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class Robot(wpilib.TimedRobot):
    """Main robot class"""
    def robotInit(self):
        """Robot initialization"""
        # Create logger
        self.logger = logging.getLogger("Robot")
        # Create timer
        self.timer = wpilib.Timer()
        # Create components list
        self.components = list()
        # Create joystick
        self.joystick = wpilib.Joystick(0)
        self.joystick_x = AnalogInput(
            self.joystick.getX,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_x)
        self.joystick_y = AnalogInput(
            self.joystick.getY,
            map_a=-1,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_y)
        self.joystick_twist = AnalogInput(
            self.joystick.getTwist,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_twist)
        # Create drivetrain
        left_0 = ctre.WPI_TalonSRX(config.Ports.Drivetrain.LEFT_0)
        left_1 = ctre.WPI_TalonSRX(config.Ports.Drivetrain.LEFT_1)
        right_0 = ctre.WPI_TalonSRX(config.Ports.Drivetrain.RIGHT_0)
        right_1 = ctre.WPI_TalonSRX(config.Ports.Drivetrain.RIGHT_1)
        self.drivetrain = Drivetrain(left_0, left_1, right_0, right_1)
        self.components.append(self.drivetrain)
        # Create shooter
        intake_motor = ctre.WPI_TalonSRX(config.Ports.Shooter.intake_m)
        intake_piston = wpilib.DoubleSolenoid(config.Ports.Shooter.intake_p)
        conveyor_motor = ctre.WPI_TalonSRX(config.Ports.Shooter.conveyor_m)
        left_shooter = ctre.WPI_TalonSRX(config.Ports.Shooter.shooter_l_m)
        right_shooter = ctre.WPI_TalonSRX(config.Ports.Shooter.shooter_r_m)
        shooter_piston_left = wpilib.DoubleSolenoid(config.Ports.Shooter.shooter_l_p)
        shooter_piston_right = wpilib.DoubleSolenoid(config.Ports.Shooter.shooter_r_p)
        prox_sensor_front = wpilib.DigitalInput(config.Ports.Shooter.prox_front)
        prox_sensor_back = wpilib.DigitalInput(config.Ports.Shooter.prox_back)
        self.shooter = Shooter(intake_motor,intake_piston,conveyor_motor,left_shooter,right_shooter,shooter_piston_left,
                                shooter_piston_right, prox_sensor_front, prox_sensor_back)
        self.components.append(self.shooter)

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
        # Run each component's execute function
        for component in self.components:
            try:
                component.execute()
            except Exception as exception:
                self.logger.exception(exception)
        # Drivetrain
        try:
            self.drivetrain.set_speeds_joystick(self.joystick_x.get(),
                                                self.joystick_y.get(),
                                                self.joystick_twist.get())
        except Exception as exception:
            self.logger.exception(exception)
    def disabledInit(self):
        """Disabled mode initialization"""

    def disabledPeriodic(self):
        """Disabled mode periodic (20ms)"""


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    wpilib.run(Robot)
