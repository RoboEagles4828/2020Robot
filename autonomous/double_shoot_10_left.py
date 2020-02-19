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

    MODE_NAME = "Double Shoot 10 Left"

    @state(first=True)
    def drive1(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED, config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() > 130.36:
            self.next_state("drive2")
    
    @state
    def drive2(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED, -config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance < -130.36:
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(config.Robot.DRIVE_TURN_SPEED,-config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() > 90:
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED, -config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() < -124.52:
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED, config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -60.845:
            self.next_state("shoot")

    @timed_state(duration=7.0, next_state="turn3")
    def shoot(self):
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)
    
    @state
    def turn3(self, initial_call):
        if initial_call:
            self.navx.reset()
            self.shooter.set_conveyor_speed(0)
            self.shooter.set_shooter_speed(0)
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED, config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -29.155:
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED, config.Robot.DRIVE_SPEED)
        self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
        if self.drivetrain.get_distance() > 95.0:
            self.next_state("turn4")

    @state
    def turn4(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(config.Robot.DRIVE_TURN_SPEED, -config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() > 70:
            self.next_state("drive5")

    @state
    def drive5(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED, config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() > 20:
            self.next_state("drive6")

    @state
    def drive6(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED, -config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance < -20:
            self.next_state("turn5")

    @state
    def turn5(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED, config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -115:
            self.next_state("drive7")

    @state
    def drive7(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SLOW_SPEED, config.Robot.DRIVE_SLOW_SPEED)
        if self.drivetrain.get_distance() > 50:
            self.next_state("turn6")

    @state
    def turn6(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED, config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -90:
            self.next_state("drive8")
        
    @state
    def drive8(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SLOW_SPEED, config.Robot.DRIVE_SLOW_SPEED)
        if self.drivetrain.get_distance() > 60:
            self.next_state("turn7")

    @state
    def turn7(self, initial_call):
        if initial_call:
            self.navx.reset()
            self.shooter.set_intake_speed(0)
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED, config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -45:
            self.next_state("drive9")

    @state
    def drive9(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED, config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() > 110:
            self.next_state("turn8")

    @state
    def turn8(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED, config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -180:
            self.next_state("shoot1")

    @timed_state(duration=7.0, next_state="end")
    def shoot1(self):
        self.drivetrain.set_speeds(0,0)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)

    @state
    def end(self):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        self.done()

