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

    MODE_NAME = "Double Shoot 6 Right"

    @state(first=True)
    def turn(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED,config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -29.155:
            self.next_state("shoot")

    @timed_state(duration=3.0, next_state="turn1")
    def shoot(self):
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)

    @state
    def turn1(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(config.Robot.DRIVE_TURN_SPEED,-config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle > 29.155:
            self.next_state("drive1")
    
    @state
    def drive1(self, initial_call):
        if initial_call:
            self.drivetrain.reset()
            self.shooter.set_conveyor_speed(0)
            self.shooter.set_shooter_speed(0)
        self.drivetrain.set_speeds(config.Robot.DRIVE_SPEED,config.Robot.DRIVE_SPEED)
        self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
        if self.drivetrain.get_distance() > 194.63:
            self.next_state("drive2")
    
    @state
    def drive2(self):
        self.drivetrain.set_speeds(-config.Robot.DRIVE_SPEED,-config.Robot.DRIVE_SPEED)
        if self.drivetrain.get_distance() < 0:
            self.next_state("turn2")
            
    @state
    def turn2(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-config.Robot.DRIVE_TURN_SPEED,config.Robot.DRIVE_TURN_SPEED)
        if self.navx.getAngle() < -29.155:
            self.next_state("shoot1")

    @timed_state(duration=7.0, next_state="end")
    def shoot1(self):
        self.drivetrain.set_speeds(0,0)
        self.shooter.set_conveyor_speed(config.Robot.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)
    
    @state
    def end(self):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        self.done()