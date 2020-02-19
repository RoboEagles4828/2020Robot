from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
import navx
from components.low.shooter import Shooter
from components.low.drivetrain import Drivetrain
class DoubleShoot6(StatefulAutonomous):
    shooter: Shooter
    drivetrain: Drivetrain
    navx: navx

    MODE_NAME = "Double Shoot 6"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot(self):
        self.shooter.set_conveyor_speed(1)
        self.shooter.set_shooter_speed(0.8)

    @state
    def drive1(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
            self.shooter.set_conveyor_speed(0)
            self.shooter.set_shooter_speed(0)
        self.drivetrain.set_speeds(0.7, 0.7)
        if self.drivetrain.get_distance() > 43.315:
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-0.3, 0.3)
        if self.navx.getAngle() % 360 > 90:
            self.next_state("drive2")

    @state
    def drive2(self):
        self.drivetrain.set_speeds(0.7,0.7)
        if self.drivetrain.get_distance() > 66.91:
            self.next_state("turn2")

    @state
    def turn2(self):
        self.drivetrain.set_speeds(0.3,-0.3)
        if self.navx.getAngle() % 360 < 0:
            self.next_state("drive3")
    
    @state
    def drive3(self, initial_call):
        if initial_call:
            self.drivetrain.reset()
        self.drivetrain.set_speeds(0.5,0.5)
        self.shooter.set_intake_speed(1)
        if self.drivetrain.get_distance() > 156.315:
            self.next_state("drive4")
    
    @state
    def drive4(self):
        self.drivetrain.set_speeds(-0.8,-0.8)
        if self.drivetrain.get_distance() < 0:
            self.next_state("turn3")
    
    @state
    def turn3(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(0.3,-0.3)
        if self.navx.getAngle() % 360 < -90:
            self.next_state("drive5")
    
    @state
    def drive5(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-0.7,-0.7)
        if self.drivetrain.get_distance() < -66.91:
            self.next_state("turn4")
    
    @state
    def turn4(self):
        self.drivetrain.set_speeds(-0.3,0.3)
        if self.navx.getAngle() % 360 > 0:
            self.next_state("drive6")

    @state
    def drive6(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(-0.7,-0.7)
        if self.drivetrain.get_distance() < -43.315:
            self.next_state("shoot1")

    @timed_state(duration=7.0)
    def shoot1(self):
        self.drivetrain.set_speeds(0,0)
        self.shooter.set_conveyor_speed(1)
        self.shooter.set_shooter_speed(0.8)