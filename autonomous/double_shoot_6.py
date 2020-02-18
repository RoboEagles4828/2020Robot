from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state


class DoubleShoot6(StatefulAutonomous):

    MODE_NAME = "Double Shoot 6"

    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot(self):
        self.shooter.set_conveyor_speed(1)
        self.shooter.set_shooter_speed(0.8)

    @state
    def drive1(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
            self.shooter.set_conveyor_speed(0)
            self.shooter.set_shooter_speed(0)
        self.drivetrain.set_speeds(0.7, 0.7)
        if self.drivetrain.get_distance() > 43.315:
            self.next_state("turn1")

    @state
    def turn1(self):
        self.drivetrain.set_speeds(-0.3, 0.3)
        if self.navx.getAngle() % 360 > 90:
            self.next_state("drive2")

    @state
    def drive2(self):
        pass
