"""Main robot module"""
import logging
import wpilib
import ctre
from navx import AHRS
from networktables import NetworkTables
from robotpy_ext.autonomous.selector import AutonomousModeSelector

import config
from autonomous.autonomous import Autonomous
from components.low.analog_input import AnalogInput
from components.low.digital_input import DigitalInput
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter
from components.low.climber import Climber
from components.high.shooter_controller import ShooterController


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
        # Create navx
        self.navx = AHRS.create_spi()
        # Create camera server
        wpilib.CameraServer.launch()
        # Create camera servos
        self.camera_servo_yaw = wpilib.Servo(config.Ports.CAMERA_SERVO_YAW)
        # Get pi network table
        self.nt_pi = NetworkTables.getTable("pi")
        # Get debug network table
        self.nt_debug = NetworkTables.getTable("debug")
        # Create buttons status
        self.button_camera = False
        self.button_intake = False
        # Create components list
        self.components = list()
        # Create joysticks
        self.joystick_0 = wpilib.Joystick(0)
        self.joystick_0_x = AnalogInput(
            self.joystick_0.getX,
            map_a=config.Robot.JOYSTICK_X_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_0_x)
        self.joystick_0_y = AnalogInput(
            self.joystick_0.getY,
            map_a=-config.Robot.JOYSTICK_Y_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_0_y)
        self.joystick_0_twist = AnalogInput(
            self.joystick_0.getTwist,
            map_a=config.Robot.JOYSTICK_TWIST_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_0_twist)
        self.joystick_1 = wpilib.Joystick(1)
        self.joystick_1_x = AnalogInput(
            self.joystick_1.getX,
            map_a=config.Robot.JOYSTICK_X_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_1_x)
        self.joystick_1_y = AnalogInput(
            self.joystick_1.getY,
            map_a=-config.Robot.JOYSTICK_Y_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_1_y)
        self.joystick_1_twist = AnalogInput(
            self.joystick_1.getTwist,
            map_a=config.Robot.JOYSTICK_TWIST_MAP_A,
            deadzone=config.Robot.JOYSTICK_DEADZONE,
            average_period=config.Robot.JOYSTICK_AVERAGE_PERIOD)
        self.components.append(self.joystick_1_twist)
        # Create drivetrain
        left_0 = ctre.WPI_TalonFX(config.Ports.Drivetrain.LEFT_0)
        left_1 = ctre.WPI_TalonFX(config.Ports.Drivetrain.LEFT_1)
        right_0 = ctre.WPI_TalonFX(config.Ports.Drivetrain.RIGHT_0)
        right_1 = ctre.WPI_TalonFX(config.Ports.Drivetrain.RIGHT_1)
        self.drivetrain = Drivetrain(left_0, left_1, right_0, right_1)
        self.components.append(self.drivetrain)
        # Create shooter
        intake = ctre.WPI_TalonSRX(config.Ports.Shooter.INTAKE)
        conveyor = ctre.WPI_VictorSPX(config.Ports.Shooter.CONVEYOR)
        conveyor_prox_front_0 = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_FRONT_0)
        conveyor_prox_front_1 = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_FRONT_1)
        conveyor_prox_back = wpilib.DigitalInput(
            config.Ports.Shooter.CONVEYOR_PROX_BACK)
        shooter_left = ctre.WPI_TalonSRX(config.Ports.Shooter.SHOOTER_LEFT)
        shooter_right = ctre.WPI_TalonSRX(config.Ports.Shooter.SHOOTER_RIGHT)
        shooter_piston_0 = wpilib.Solenoid(
            config.Ports.Shooter.SHOOTER_PISTON_0)
        shooter_piston_1 = wpilib.Solenoid(
            config.Ports.Shooter.SHOOTER_PISTON_1)
        self.shooter = Shooter(intake, conveyor, conveyor_prox_front_0,
                               conveyor_prox_front_1, conveyor_prox_back,
                               shooter_left, shooter_right, shooter_piston_0,
                               shooter_piston_1)
        self.components.append(self.shooter)
        # Create climber
        climber_left = ctre.WPI_TalonSRX(config.Ports.Climber.CLIMBER_LEFT)
        climber_right = ctre.WPI_TalonSRX(config.Ports.Climber.CLIMBER_RIGHT)
        winch_left_front = ctre.WPI_VictorSPX(
            config.Ports.Climber.WINCH_LEFT_FRONT)
        winch_left_back = ctre.WPI_VictorSPX(
            config.Ports.Climber.WINCH_LEFT_BACK)
        winch_right_front = ctre.WPI_VictorSPX(
            config.Ports.Climber.WINCH_RIGHT_FRONT)
        winch_right_back = ctre.WPI_VictorSPX(
            config.Ports.Climber.WINCH_RIGHT_BACK)
        self.climber = Climber(climber_left, climber_right, winch_left_front,
                               winch_left_back, winch_right_front,
                               winch_right_back)
        self.components.append(self.climber)
        # Create shooter controller
        self.shooter_controller = ShooterController(self.shooter)
        self.components.append(self.shooter_controller)
        # Create autonomous helper
        self.autonomous = Autonomous(self.drivetrain, self.navx,
                                     self.shooter_controller)
        # Create autonomous selector
        self.auton_mode = AutonomousModeSelector(
            "autonomous", {
                "autonomous": self.autonomous,
                "drivetrain": self.drivetrain,
                "navx": self.navx,
                "shooter": self.shooter,
                "shooter_controller": self.shooter_controller,
                "nt_pi": self.nt_pi
            })

    def autonomousInit(self):
        """Autonomous mode initialization"""
        self.shooter_controller.enable()

    def autonomousPeriodic(self):
        try:
            self.auton_mode.run(iter_fn=self.autonomous_iter)
        except Exception as exception:
            self.logger.exception(exception)

    def autonomous_iter(self):
        """Autonomous mode periodic (20ms)"""
        # Run each component's execute function
        for component in self.components:
            try:
                component.execute()
            except Exception as exception:
                self.logger.exception(exception)

    def teleopInit(self):
        """Teleoperated mode initialization"""
        self.timer.reset()
        self.timer.start()
        self.shooter_controller.enable()

    def teleopPeriodic(self):
        """Teleoperated mode periodic (20ms)"""
        # Run each component's execute function
        for component in self.components:
            try:
                component.execute()
            except Exception as exception:
                self.logger.exception(exception)
        # Camera
        try:
            button = self.joystick_0.getRawButton(
                config.Buttons.Joystick0.CAMERA)
            if button and not self.button_camera:
                self.camera_servo_yaw.set(
                    config.Robot.CAMERA_YAW_POS_0 if self.camera_servo_yaw.get(
                    ) == config.Robot.CAMERA_YAW_POS_1 else config.Robot.
                    CAMERA_YAW_POS_1)
            self.button_camera = button
        except Exception as exception:
            self.logger.exception(exception)
        # Drivetrain
        try:
            if self.joystick_0.getRawButton(
                    config.Buttons.Joystick0.Drivetrain.VISION):
                value = self.nt_pi.getNumber(
                    "value", 0) * config.Robot.Drivetrain.VISION_RATIO
                if abs(value) < config.Robot.Drivetrain.VISION_MIN_SPEED:
                    value = value / abs(
                        value) * config.Robot.Drivetrain.VISION_MIN_SPEED
                if abs(value) < config.Robot.Drivetrain.VISION_CUTOFF:
                    value = 0
                self.drivetrain.set_speeds(value, -value)
            else:
                self.drivetrain.set_speeds_joystick(
                    0, self.joystick_0_y.get(), self.joystick_0_twist.get())
        except Exception as exception:
            self.logger.exception(exception)
        # Shooter
        try:
            # Intake (Joystick 1)
            button = self.joystick_1.getRawButton(
                config.Buttons.Joystick1.Shooter.INTAKE)
            if button and not self.button_intake:
                self.shooter.set_intake_speed(
                    config.Robot.Shooter.INTAKE_SPEED if self.shooter.
                    get_intake_speed() == 0 else 0)
            self.button_intake = button
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Shooter.OUTTAKE):
                self.shooter.set_intake_speed(
                    -config.Robot.Shooter.OUTTAKE_SPEED)
            elif self.shooter.get_intake_speed() < 0:
                self.shooter.set_intake_speed(0)
            # Conveyor
            self.shooter.set_conveyor(
                self.joystick_0.getRawButton(
                    config.Buttons.Joystick0.Shooter.CONVEYOR))
            # Shooter (Joystick 1)
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Shooter.SHOOT_0):
                self.shooter_controller.set_velocity(
                    config.Robot.ShooterController.SHOOTER_VELOCITY_0)
            elif self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Shooter.SHOOT_1):
                self.shooter_controller.set_velocity(
                    config.Robot.ShooterController.SHOOTER_VELOCITY_2)
            else:
                self.shooter_controller.set_velocity(0)
            # Shooter status (Joystick 0)
            if self.joystick_0.getPOV() == 180:
                self.shooter.set_shooter(True)
            elif self.joystick_0.getPOV() == 0:
                self.shooter.set_shooter(False)
        except Exception as exception:
            self.logger.exception(exception)
        # Climber
        try:
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.LEFT_UP):
                self.climber.set_climber_left_speed(
                    config.Robot.Climber.CLIMBER_LEFT_UP_SPEED)
                self.climber.set_winch_left_front_speed(
                    config.Robot.Climber.WINCH_LEFT_FRONT_UP_SPEED)
                self.climber.set_winch_left_back_speed(
                    config.Robot.Climber.WINCH_LEFT_BACK_UP_SPEED)
            elif self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.LEFT_DOWN):
                self.climber.set_climber_left_speed(
                    -config.Robot.Climber.CLIMBER_LEFT_DOWN_SPEED)
                self.climber.set_winch_left_front_speed(
                    -config.Robot.Climber.WINCH_LEFT_FRONT_DOWN_SPEED)
                self.climber.set_winch_left_back_speed(
                    -config.Robot.Climber.WINCH_LEFT_BACK_DOWN_SPEED)
            else:
                self.climber.set_climber_left_speed(0)
                self.climber.set_winch_left_front_speed(0)
                self.climber.set_winch_left_back_speed(0)
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.WINCH_LEFT_FRONT):
                self.climber.set_winch_left_front_speed(
                    config.Robot.Climber.WINCH_LEFT_FRONT_UP_SPEED
                    if self.joystick_1.getThrottle() < 0 else
                    -config.Robot.Climber.WINCH_LEFT_FRONT_DOWN_SPEED)
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.WINCH_LEFT_BACK):
                self.climber.set_winch_left_back_speed(
                    config.Robot.Climber.WINCH_LEFT_BACK_UP_SPEED
                    if self.joystick_1.getThrottle() < 0 else
                    -config.Robot.Climber.WINCH_LEFT_BACK_DOWN_SPEED)
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.RIGHT_UP):
                self.climber.set_climber_right_speed(
                    config.Robot.Climber.CLIMBER_RIGHT_UP_SPEED)
                self.climber.set_winch_right_front_speed(
                    config.Robot.Climber.WINCH_RIGHT_FRONT_UP_SPEED)
                self.climber.set_winch_right_back_speed(
                    config.Robot.Climber.WINCH_RIGHT_BACK_UP_SPEED)
            elif self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.RIGHT_DOWN):
                self.climber.set_climber_right_speed(
                    -config.Robot.Climber.CLIMBER_RIGHT_DOWN_SPEED)
                self.climber.set_winch_right_front_speed(
                    -config.Robot.Climber.WINCH_RIGHT_FRONT_DOWN_SPEED)
                self.climber.set_winch_right_back_speed(
                    -config.Robot.Climber.WINCH_RIGHT_BACK_DOWN_SPEED)
            else:
                self.climber.set_climber_right_speed(0)
                self.climber.set_winch_right_front_speed(0)
                self.climber.set_winch_right_back_speed(0)
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.WINCH_RIGHT_FRONT):
                self.climber.set_winch_right_front_speed(
                    config.Robot.Climber.WINCH_RIGHT_FRONT_UP_SPEED
                    if self.joystick_1.getThrottle() < 0 else
                    -config.Robot.Climber.WINCH_RIGHT_FRONT_DOWN_SPEED)
            if self.joystick_1.getRawButton(
                    config.Buttons.Joystick1.Climber.WINCH_RIGHT_BACK):
                self.climber.set_winch_right_back_speed(
                    config.Robot.Climber.WINCH_RIGHT_BACK_UP_SPEED
                    if self.joystick_1.getThrottle() < 0 else
                    -config.Robot.Climber.WINCH_RIGHT_BACK_DOWN_SPEED)
        except Exception as exception:
            self.logger.exception(exception)

    def disabledInit(self):
        """Disabled mode initialization"""

    def disabledPeriodic(self):
        """Disabled mode periodic (20ms)"""


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    wpilib.run(Robot)
