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

    MODE_NAME = "Double Shoot 6 Right"

    @state(first=True)
    def turn(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-0.3,0.3)
        if self.navx.getAngle() > 29.155:
            self.next_state("shoot")

    @timed_state(duration=3.0, next_state="turn1")
    def shoot(self):
        self.shooter.set_conveyor_speed(1)
        self.shooter.set_shooter_speed(0.8)

    @state
    def turn1(self):
        self.drivetrain.set_speeds(0.3,-0.3)
        if self.navx.getAngle < 0:
            self.next_state("drive1")
    
    @state
    def drive1(self, initial_call):
        if initial_call:
            self.drivetrain.reset()
            self.shooter.set_conveyor_speed(0)
            self.shooter.set_shooter_speed(0)
        self.drivetrain.set_speeds(0.5,0.5)
        self.shooter.set_intake_speed(1)
        if self.drivetrain.get_distance() > 194.63:
            self.next_state("drive2")
    
    @state
    def drive2(self):
        self.drivetrain.set_speeds(-0.8,-0.8)
        if self.drivetrain.get_distance() < 0:
            self.next_state("turn2")
            
    @state
    def turn2(self, initial_call):
        if initial_call:
            self.navx.reset()
        self.drivetrain.set_speeds(-0.3,0.3)
        if self.navx.getAngle() > 29.155:
            self.next_state("shoot1")

    @timed_state(duration=7.0)
    def shoot1(self):
        self.drivetrain.set_speeds(0,0)
        self.shooter.set_conveyor_speed(1)
        self.shooter.set_shooter_speed(0.8)