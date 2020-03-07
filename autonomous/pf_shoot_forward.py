from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter
from components.high.auto_drivetrain import AutoDrivetrain


class PFShootForward(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter
    auto_drivetrain: AutoDrivetrain

    MODE_NAME = "PF Shoot Forward"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot1(self):
        self.autonomous.shoot_0()

    @state
    def drive1(self, initial_call):
        if initial_call:
            self.auto_drivetrain.set_path("shoot_forward")
            self.auto_drivetrain.enable()
        if self.auto_drivetrain.is_finished():
            self.next_state("end")

    @state
    def end(self):
        self.auto_drivetrain.disable()
        self.drivetrain.set_speeds(0, 0)
