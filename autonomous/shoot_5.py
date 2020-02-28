from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class Shoot5(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter

    MODE_NAME = "Shoot 5"

    @state(first=True)
    def drive1(self, initial_call):
        self.shooter.set_intake_speed(config.Robot.Shooter.INTAKE_SPEED)
        if self.autonomous.drive(initial_call, config.Autonomous.POS_3_TRENCH):
            self.next_state("drive2")

    @state
    def drive2(self, initial_call):
        self.shooter.set_intake_speed(0)
        self.shooter.set_shooter(False)
        if self.autonomous.drive(initial_call,
                                 -config.Autonomous.POS_3_TRENCH):
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, 90):
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        if self.autonomous.drive(initial_call, -config.Autonomous.POS_3_SHOOT):
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_3_TURN):
            self.next_state("shoot1")

    @timed_state(duration=5.0, next_state="turn3")
    def shoot1(self):
        self.autonomous.shoot()

    @state
    def turn3(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_2_TURN):
            self.next_state("end")

    @state
    def end(self):
        self.drivetrain.set_speeds(0, 0)
        self.done()
