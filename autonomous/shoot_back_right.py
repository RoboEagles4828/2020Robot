from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class ShootBackRight(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter

    MODE_NAME = "Shoot Back Right"

    @state(first=True)
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, -config.Autonomous.POS_2_TURN):
            self.next_state("shoot1")

    @timed_state(duration=3.0, next_state="turn2")
    def shoot1(self):
        self.autonomous.shoot()

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, config.Autonomous.POS_2_TURN):
            self.next_state("drive1")

    @state
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call,
                                 -config.Autonomous.DRIVE_DISTANCE):
            self.next_state("end")

    @state
    def end(self):
        self.drivetrain.set_speeds(0, 0)
        self.done()
