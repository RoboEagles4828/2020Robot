from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS
from networktables import NetworkTable

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class Shoot5Mid(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter
    nt_pi: NetworkTable

    MODE_NAME = "Shoot 5 Mid"

    @timed_state(duration=3.0, next_state="turn1", first=True)
    def shoot1(self):
        self.autonomous.shoot_0()

    @state
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, -10):
            self.next_state("drive1")
    @state
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call, 130):
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, 110):
            self.next_state("drive2")

    @state
    def drive2(self, initial_call):
        self.shooter.set_intake_speed(config.Robot.Shooter.INTAKE_SPEED)
        if self.autonomous.drive(initial_call, 24):
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        self.shooter.set_intake_speed(0)
        if self.autonomous.drive(initial_call, -24):
            self.next_state("turn3")

    @state
    def turn3(self, initial_call):
        if self.autonomous.turn(initial_call, -110):
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        if self.autonomous.drive(initial_call, -130):
            self.next_state("vision1")

    @timed_state(duration=1.0, next_state="shoot2")
    def vision1(self):
        value = self.nt_pi.getNumber("value",
                                     0) * config.Robot.Drivetrain.VISION_RATIO
        if abs(value) < 0.05:
            value = value / abs(value) * 0.05
        self.drivetrain.set_speeds(value, -value)

    @timed_state(duration=3.0, next_state="end")
    def shoot2(self):
        self.autonomous.shoot_0()

    @state
    def end(self):
        self.drivetrain.set_speeds(0,0)
        self.done()
    """@timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot1(self):
        self.autonomous.shoot_0()

    @state
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call, -config.Autonomous.DS_SHOOT):
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call,
                                config.Autonomous.DS_8_TURN-90):
            self.next_state("drive2")
    @state
    def drive2(self, initial_call):
        self.shooter.set_intake_speed(config.Robot.Shooter.INTAKE_SPEED)
        if self.autonomous.drive(initial_call,
                                 config.Autonomous.DS_8_FORWARD_MID,
                                 slow=True):
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        self.shooter.set_intake_speed(0)
        self.shooter.set_shooter(False)
        if self.autonomous.drive(initial_call,
                                 -config.Autonomous.DS_8_BACK_MID,
                                 slow=True):
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call,
                                90-config.Autonomous.DS_8_TURN):
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        if self.autonomous.drive(initial_call, config.Autonomous.DS_SHOOT):
            self.next_state("turn3")

    @state
    def turn3(self, initial_call):
        if self.autonomous.turn(initial_call, 180):
            self.next_state("shoot2")

    @timed_state(duration=5.0, next_state="end")
    def shoot2(self):
        self.autonomous.shoot_0()

    @state
    def end(self):
        self.shooter.set_shooter_speed(0)
        self.done()"""
