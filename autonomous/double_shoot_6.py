from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous.autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter
from components.high.shooter_controller import ShooterController


class DoubleShoot6(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter
    shooter_controller: ShooterController

    MODE_NAME = "Double Shoot 6"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot1(self):
        self.autonomous.shoot_0()

    @state
    def drive1(self, initial_call):
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
        self.shooter.set_intake_speed(config.Robot.Shooter.INTAKE_SPEED)
        if self.autonomous.drive(initial_call,
                                 config.Autonomous.POS_1_TRENCH,
                                 slow=True):
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        self.shooter.set_intake_speed(0)
        self.shooter.set_shooter(False)
        if self.autonomous.drive(initial_call,
                                 -config.Autonomous.POS_2_TRENCH):
            self.next_state("turn3")

    @state
    def turn3(self, initial_call):
        if self.autonomous.turn(initial_call,
                                -config.Autonomous.POS_2_TRENCH_TURN):
            self.next_state("vision1")

    @timed_state(duration=1.5, next_state="shoot2")
    def vision1(self):
        self.autonomous.vision()

    @timed_state(duration=3.0, next_state="end")
    def shoot2(self):
        self.autonomous.shoot_1()

    @state
    def end(self):
        self.shooter_controller.set_velocity(0)
        self.done()
