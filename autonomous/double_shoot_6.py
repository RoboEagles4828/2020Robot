from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
import navx
from components.low.shooter import Shooter
from components.low.drivetrain import Drivetrain
import config
class DoubleShoot6(StatefulAutonomous):
    shooter: Shooter
    drivetrain: Drivetrain
    navx: navx
    MODE_NAME = "Double Shoot 6"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot1(self):
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)

    @state
    def drive1(self, initial_call):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED,
                                   config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() > 43.315:
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED,
                                   config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() % 360 < -90:
            self.next_state("drive2")

    @state
    def drive2(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED,
                                   config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() > 66.91:
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(config.Robot.DRIVE_TURN_SPEED,
                                   -config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() % 360 > 90:
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        if initial_call:
            self.drivetrain.reset()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED,
                                   config.Robot.DRIVE_SPEED)
        self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
        if self.drivetrain.get_distance() > 156.315:
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        if initial_call:
            self.drivetrain.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED,
                                   -config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() < -156.315:
            self.next_state("turn3")

    @state
    def turn3(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(config.Robot.DRIVE_TURN_SPEED,
                                   -config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() % 360 > 90:
            self.next_state("drive5")

    @state
    def drive5(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED,
                                   -config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() < -66.91:
            self.next_state("turn4")

    @state
    def turn4(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED,
                                   config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() % 360 < -90:
            self.next_state("drive6")

    @state
    def drive6(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED,
                                   -config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() < -43.315:
            self.next_state("shoot2")

    @timed_state(duration=5.0, next_state="end")
    def shoot2(self):
        self.drivetrain.set_speeds(0, 0)
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)

    @state
    def end(self):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        self.done()