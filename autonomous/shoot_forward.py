from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class ShootForward(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter

    MODE_NAME = "Shoot Forward"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot1(self):
        self.autonomous.shoot_0()

    @state
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call,
                                 config.Autonomous.DRIVE_DISTANCE):
            self.next_state("end")

    @state
    def end(self):
        self.drivetrain.set_speeds(0, 0)
