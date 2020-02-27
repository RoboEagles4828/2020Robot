"""Main robot module"""
import logging
import wpilib
import ctre
from networktables import NetworkTables

import config
from components.low.analog_input import AnalogInput
from components.low.digital_input import DigitalInput
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter
from components.low.climber import Climber


class Robot(wpilib.TimedRobot):
    """Main robot class"""
    def robotInit(self):
        """Robot initialization"""
        # Create logger
        self.logger = logging.getLogger("Robot")
        # Create timer
        self.timer = wpilib.Timer()
        # Create compressor
        wpilib.Compressor(0).setClosedLoopControl(True)
        # Create camera server
        wpilib.CameraServer.launch()
        # Create camera servos
        self.camera_servo_yaw = wpilib.Servo(config.Ports.CAMERA_SERVO_YAW)
        self.camera_servo_pitch = wpilib.Servo(config.Ports.CAMERA_SERVO_PITCH)
        # Get pi network table
        self.nt_pi = NetworkTables.getTable("pi")
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
        intake_control = ctre.WPI_VictorSPX(
            config.Ports.Shooter.INTAKE_CONTROL)
        conveyor = ctre.WPI_VictorSPX(config.Ports.Shooter.CONVEYOR)
        conveyor_prox_front = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_FRONT)
        conveyor_prox_back = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_BACK)
        shooter_left = ctre.WPI_TalonSRX(config.Ports.Shooter.SHOOTER_LEFT)
        shooter_right = ctre.WPI_TalonSRX(config.Ports.Shooter.SHOOTER_RIGHT)
        shooter_piston_0 = wpilib.Solenoid(
            config.Ports.Shooter.SHOOTER_PISTON_0)
        shooter_piston_1 = wpilib.Solenoid(
            config.Ports.Shooter.SHOOTER_PISTON_1)
        self.shooter = Shooter(intake, intake_control, conveyor,
                               conveyor_prox_front, conveyor_prox_back,
                               shooter_left, shooter_right, shooter_piston_0,
                               shooter_piston_1)
        self.components.append(self.shooter)
        # Create climber
        climber_0 = ctre.WPI_TalonSRX(config.Ports.Climber.CLIMBER_0)
        climber_1 = ctre.WPI_TalonSRX(config.Ports.Climber.CLIMBER_1)
        winch_0_0 = ctre.WPI_TalonSRX(config.Ports.Climber.WINCH_0_0)
        winch_0_1 = ctre.WPI_TalonSRX(config.Ports.Climber.WINCH_0_1)
        winch_1_0 = ctre.WPI_TalonSRX(config.Ports.Climber.WINCH_1_0)
        winch_1_1 = ctre.WPI_VictorSPX(config.Ports.Climber.WINCH_1_1)
        self.climber = Climber(climber_0, climber_1, winch_0_0, winch_0_1,
                               winch_1_0, winch_1_1)
        self.components.append(self.climber)

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
            if self.joystick.getRawButton(config.Buttons.Drivetrain.VISION):
                value = self.nt_pi.getNumber("value",
                                             0) * config.Robot.VISION_RATIO
                self.drivetrain.set_speeds(value, -value)
            else:
                self.drivetrain.set_speeds_joystick(self.joystick_x.get(),
                                                    self.joystick_y.get(),
                                                    self.joystick_twist.get())
        except Exception as exception:
            self.logger.exception(exception)
        # Shooter
        try:
            if self.joystick.getRawButton(config.Buttons.Shooter.INTAKE):
                self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
            elif self.joystick.getRawButton(config.Buttons.Shooter.OUTTAKE):
                self.shooter.set_intake_speed(-config.Robot.INTAKE_SPEED)
            else:
                self.shooter.set_intake_speed(0)
            if self.joystick.getRawButton(config.Buttons.Shooter.SHOOTER):
                self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)
            else:
                self.shooter.set_shooter_speed(0)
            if self.joystick.getPOV() == 180:
                self.shooter.set_shooter(True)
            elif self.joystick.getPOV() == 0:
                self.shooter.set_shooter(False)
        except Exception as exception:
            self.logger.exception(exception)
        # Climber
        try:
            if self.joystick.getRawButton(config.Buttons.Climber.UP):
                self.climber.set_climber_speed(config.Robot.CLIMBER_SPEED)
                self.climber.set_winch_speed(config.Robot.WINCH_SPEED)
            elif self.joystick.getRawButton(config.Buttons.Climber.DOWN):
                self.climber.set_climber_speed(-config.Robot.CLIMBER_SPEED)
                self.climber.set_winch_speed(-config.Robot.WINCH_SPEED)
            else:
                self.climber.set_climber_speed(0)
                self.climber.set_winch_speed(0)
        except Exception as exception:
            self.logger.exception(exception)

    def disabledInit(self):
        """Disabled mode initialization"""

    def disabledPeriodic(self):
        """Disabled mode periodic (20ms)"""


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    wpilib.run(Robot)
