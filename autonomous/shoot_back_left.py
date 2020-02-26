from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class ShootBackLeft(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter

    MODE_NAME = "Shoot Back Left"

    @state(first=True)
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, 90):
            self.next_state("drive1")

    @state
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call, -config.Autonomous.POS_3_SHOOT):
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_3_TURN):
            self.next_state("shoot1")

    @timed_state(duration=3.0, next_state="turn3")
    def shoot1(self):
        self.autonomous.shoot()

    @state
    def turn3(self, initial_call):
        if self.autonomous.turn(initial_call,
                                90 - config.Autonomous.POS_3_TURN):
            self.next_state("drive2")

    @state
    def drive2(self, initial_call):
        if self.autonomous.drive(initial_call,
                                 -config.Autonomous.DRIVE_DISTANCE):
            self.next_state("end")

    @state
    def end(self):
        self.drivetrain.set_speeds(0, 0)
        self.done()
