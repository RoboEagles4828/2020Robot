from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS
from networktables import NetworkTable

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class ShootForwardVision(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter
    nt_pi: NetworkTable

    MODE_NAME = "Shoot Forward Vision"

    @timed_state(duration=1.0, next_state="shoot1", first=True)
    def vision1(self):
        value = self.nt_pi.getNumber("value",
                                     0) * config.Robot.Drivetrain.VISION_RATIO
        if abs(value) < 0.05:
            value = value / abs(value) * 0.05
        self.drivetrain.set_speeds(value, -value)

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
