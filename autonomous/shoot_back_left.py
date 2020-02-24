from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
import navx
from autonomous import Autonomous
from components.low.shooter import Shooter
from components.low.drivetrain import Drivetrain
import config
class ShootBackLeft(StatefulAutonomous):
    autonomous: Autonomous
    shooter: Shooter
    drivetrain: Drivetrain
    navx: navx

    MODE_NAME = "Shoot 3 Go Back Left"
    
    @state(first=True)
    def turn(self, initial_call):
        if self.autonomous.turn(initial_call, 90):
            self.next_state("drive")

    @state
    def drive(self, initial_call):
        if self.autonomous.drive(initial_call, -config.Autonomous.POS_3_SHOOT):
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_3_TURN):
            self.next_state("shoot")
    
    @timed_state(duration=3.0, next_state="turn2")
    def shoot(self, initial_call):
        self.autonomous.shoot(initial_call)

    @state
    def turn2(self, initial_call):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        if self.autonomous.turn(initial_call, 90-config.Autonomous.POS_3_TURN):
            self.next_state("drive1")
    
    @state
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call, -config.Autonomous.DRIVE_DISTANCE):
            self.next_state("end")
    
    @state
    def end(self):
        self.drivetrain.set_speeds(0,0)
        self.done()