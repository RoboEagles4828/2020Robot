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
            map_a=config.Robot.JOYSTICK_X_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_x)
        self.joystick_y = AnalogInput(
            self.joystick.getY,
            map_a=-config.Robot.JOYSTICK_Y_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_y)
        self.joystick_twist = AnalogInput(
            self.joystick.getTwist,
            map_a=config.Robot.JOYSTICK_TWIST_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_twist)
        # Create drivetrain
        left_0 = ctre.WPI_TalonFX(config.Ports.Drivetrain.LEFT_0)
        left_1 = ctre.WPI_TalonFX(config.Ports.Drivetrain.LEFT_1)
        right_0 = ctre.WPI_TalonFX(config.Ports.Drivetrain.RIGHT_0)
        right_1 = ctre.WPI_TalonFX(config.Ports.Drivetrain.RIGHT_1)
        self.drivetrain = Drivetrain(left_0, left_1, right_0, right_1)
        self.components.append(self.drivetrain)
        # Create shooter
        intake = ctre.WPI_TalonSRX(config.Ports.Shooter.INTAKE)
        intake_piston = wpilib.DoubleSolenoid(
            config.Ports.Shooter.INTAKE_PISTON)
        conveyor = ctre.WPI_TalonSRX(config.Ports.Shooter.CONVEYOR)
        conveyor_prox_front = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_FRONT)
        conveyor_prox_back = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_BACK)
        shooter_left = ctre.WPI_TalonSRX(config.Ports.Shooter.SHOOTER_LEFT)
        shooter_right = ctre.WPI_TalonSRX(config.Ports.Shooter.SHOOTER_RIGHT)
        shooter_piston_0 = wpilib.DoubleSolenoid(
            config.Ports.Shooter.SHOOTER_PISTON_0)
        shooter_piston_1 = wpilib.DoubleSolenoid(
            config.Ports.Shooter.SHOOTER_PISTON_1)
        self.shooter = Shooter(intake, intake_piston, conveyor,
                               conveyor_prox_front, conveyor_prox_back,
                               shooter_left, shooter_right, shooter_piston_0,
                               shooter_piston_1)
        self.components.append(self.shooter)

    def autonomousInit(self):
        """Autonomous mode initialization"""
        self.pos1 = False
        self.pos2 = False
        self.navx.reset()
        self.navx.resetDisplacement()
        self.drivetrain.reset_distance()
        
    def autonomousPeriodic(self):
        """Autonomous mode periodic (20ms)"""
     # Run each component's execute function
        for component in self.components:
            try:
                component.execute()
            except Exception as exception:
                self.logger.exception(exception)
        # Auton mode 1
        try:
            if self.drivetrain.get_distance() >= 0 or self.drivetrain.get_distance() <= 5:
                self.shooter.set_shooter_speed(0.8)
                self.shooter.set_conveyor_speed(1)
                self.drivetrain.reset_distance()
            elif  self.drivetrain.get_distance() < 56.315 and not self.pos1:
                self.drivetrain.set_speeds(0.7, 0.7)
                self.shooter.set_shooter_speed(0)
                self.shooter.set_conveyor_speed(0)
            elif self.navx.getAngle() % 360 < 90:
                self.pos1 = True
                self.drivetrain.reset_distance()
                self.drivetrain.set_speeds(-0.3, 0.3)
            elif self.drivetrain.get_distance() < 66.91 and not self.pos2:
                self.drivetrain.set_speeds(0.7, 0.7)
            elif self.navx.getAngle() % 360 > 0:
                self.pos2 = True
                self.drivetrain.reset_distance()
                self.drivetrain.set_speeds(0.3, -0.3)
            elif self.drivetrain.get_distance() <= 138.315:
                self.drivetrain.set_speeds(0.5, 0.5)
                self.shooter.set_intake_speed(1)
            elif self.drivetrain.get_distance() > 0:
                self.drivetrain.set_speeds(-0.5,-0.5)
                self.shooter.set_intake_speed(0)
                self.navx.reset()
            elif self.navx.getAngle() % 360 > -90:
                self.drivetrain.reset_distance()
                self.drivetrain.set_speeds(0.3,-0.3)
            elif self.drivetrain.get_distance() > -66.91 and self.pos1:
                self.drivetrain.set_speeds(-0.7,-0.7)
            elif self.navx.getAngle() % 360 < 0:
                self.drivetrain.reset_distance()
                self.drivetrain.set_speeds(-0.3,0.3)
                self.pos1 = False
            elif self.drivetrain.get_distance() > -43.315:
                self.drivetrain.set_speeds(-0.7,-0.7)
            elif self.drivetrain.get_distance() < 100:
                self.shooter.set_shooter_speed(0.8)
                self.shooter.set_conveyor_speed(1)
            else:
                self.drivetrain.set_speeds(0, 0)
                self.shooter.set_shooter_speed(0)
                self.shooter.set_intake_speed(0)
                self.shooter.set_conveyor_speed(0)
        except Exception as exception:
            self.logger.exception(exception)
        # Auton Mode 2
        try:
            if True:
                pass
        except Exception as exception:
            self.logger.exception(exception)
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
        # Shooter
        try:
            if self.joystick.getRawButton(config.Buttons.Shooter.INTAKE):
                self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
            else:
                self.shooter.set_intake_speed(0)
            if self.joystick.getRawButton(config.Buttons.Shooter.SHOOTER):
                self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
                self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)
            else:
                self.shooter.set_conveyor_speed(0)
                self.shooter.set_shooter_speed(0)
        except Exception as exception:
            self.logger.exception(exception)

    def disabledInit(self):
        """Disabled mode initialization"""

    def disabledPeriodic(self):
        """Disabled mode periodic (20ms)"""


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    wpilib.run(Robot)
