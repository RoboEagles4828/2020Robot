from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
import navx
from autonomous import Autonomous
from components.low.shooter import Shooter
from components.low.drivetrain import Drivetrain
import config
class DoubleShoot6Right(StatefulAutonomous):
    autonomous: Autonomous
    shooter: Shooter
    drivetrain: Drivetrain
    navx: navx

    MODE_NAME = "Double Shoot 6 Right"

    @state(first=True)
    def turn(self, initial_call):
        if self.autonomous.turn(-config.Autonomous.POS_2_TURN):
            self.next_state("shoot")

    @timed_state(duration=3.0, next_state="turn1")
    def shoot(self, initial_call):
        self.autonomous.shoot(initial_call)

    @state
    def turn1(self, initial_call):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        if self.autonomous.turn(initial_call, config.Autonomous.POS_2_TURN):
            self.next_state("drive1")
    
    @state
    def drive1(self, initial_call):
        self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
        if self.autonomous.drive(initial_call, config.Autonomous.POS_2_TRENCH):
            self.next_state("drive2")
    
    @state
    def drive2(self, initial_call):
        self.shooter.set_intake_speed(0)
        if self.autonomous.drive(initial_call, -config.Autonomous.POS_2_TRENCH):
            self.next_state("turn2")
            
    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_2_TURN):
            self.next_state("shoot1")

    @timed_state(duration=7.0, next_state="end")
    def shoot1(self, initial_call):
        self.autonomous.shoot(initial_call)
    
    @state
    def end(self):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        self.done()