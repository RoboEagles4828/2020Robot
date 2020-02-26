from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
from navx import AHRS

import config
from autonomous import Autonomous
from components.low.drivetrain import Drivetrain
from components.low.shooter import Shooter


class DoubleShoot10Left(StatefulAutonomous):

    autonomous: Autonomous
    drivetrain: Drivetrain
    navx: AHRS
    shooter: Shooter

    MODE_NAME = "Double Shoot 10 Left"

    @state(first=True)
    def drive1(self, initial_call):
        if self.autonomous.drive(initial_call, 130.4):
            self.next_state("drive2")

    @state
    def drive2(self, initial_call):
        if self.autonomous.drive(initial_call, -130.4):
            self.next_state("turn1")

    @state
    def turn1(self, initial_call):
        if self.autonomous.turn(initial_call, 90):
            self.next_state("drive3")

    @state
    def drive3(self, initial_call):
        if self.autonomous.drive(initial_call, -124.5):
            self.next_state("turn2")

    @state
    def turn2(self, initial_call):
        if self.autonomous.turn(initial_call, -60.8):
            self.next_state("shoot1")

    @timed_state(duration=7.0, next_state="turn3")
    def shoot1(self):
        self.drivetrain.set_speeds(0, 0)
        self.shooter.set_conveyor_speed(config.Shooter.CONVEYOR_SPEED)
        self.shooter.set_shooter_speed(config.Robot.SHOOTER_SPEED)

    @state
    def turn3(self, initial_call):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        if self.autonomous.turn(initial_call, -29.2):
            self.next_state("drive4")

    @state
    def drive4(self, initial_call):
        self.shooter.set_intake_speed(config.Robot.INTAKE_SPEED)
        if self.autonomous.drive(initial_call, 95.0):
            self.next_state("turn4")

    @state
    def turn4(self, initial_call):
        if self.autonomous.turn(initial_call, 70):
            self.next_state("drive5")

    @state
    def drive5(self, initial_call):
        if self.autonomous.drive(initial_call, 20):
            self.next_state("drive6")

    @state
    def drive6(self, initial_call):
        if self.autonomous.drive(initial_call, -20):
            self.next_state("turn5")

    @state
    def turn5(self, initial_call):
        if self.autonomous.turn(initial_call, -115):
            self.next_state("drive7")

    @state
    def drive7(self, initial_call):
        if self.autonomous.drive(initial_call, 50, slow=True):
            self.next_state("turn6")

    @state
    def turn6(self, initial_call):
        if self.autonomous.turn(initial_call, -90):
            self.next_state("drive8")

    @state
    def drive8(self, initial_call):
        if self.autonomous.drive(initial_call, 60, slow=True):
            self.next_state("turn7")

    @state
    def turn7(self, initial_call):
        self.shooter.set_intake_speed(0)
        if self.autonomous.turn(initial_call, -45):
            self.next_state("drive9")

    @state
    def drive9(self, initial_call):
        if self.autonomous.drive(initial_call, 110):
            self.next_state("turn8")

    @state
    def turn8(self, initial_call):
        if self.autonomous.turn(initial_call, -180):
            self.next_state("shoot2")

    @timed_state(duration=7.0, next_state="end")
    def shoot2(self, initial_call):
        self.autonomous.shoot(initial_call)

    @state
    def end(self):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        self.done()
