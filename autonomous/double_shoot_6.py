from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class DoubleShoot6(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter

    MODE_NAME = "Double Shoot 6"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot1(self):
        self.autonomous.shoot()

    @state
    def drive1(self, initial_call):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        if self.autonomous.drive(initial_call,
                                 config.Autonomous.POS_1_FORWARD):
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, -90):
            self.next_state("drive2")

    @state
    def drive2(self, initial_call):
        if self.autonomous.drive(initial_call,
                                 config.Autonomous.POS_1_TO_TRENCH):
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, 90):
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
        if self.autonomous.drive(initial_call, config.Autonomous.POS_1_TRENCH):
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        self.shooter.set_intake_speed(0)
        if self.autonomous.drive(initial_call,
                                 -config.Autonomous.POS_2_TRENCH):
            self.next_state("turn3")
    
    @state
    def turn3(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_2_TRENCH_TURN):
            self.next_state("shoot2")

    @timed_state(duration=5.0, next_state="end")
    def shoot2(self, initial_call):
        self.autonomous.shoot(initial_call)

    @state
    def end(self):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        self.done()
