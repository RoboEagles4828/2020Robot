from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
import navx
from components.low.shooter import Shooter
from components.low.drivetrain import Drivetrain
class DoubleShoot6(StatefulAutonomous):
    shooter: Shooter
    drivetrain: Drivetrain
    navx: navx

    MODE_NAME = "Shoot 3 Go Forward"
    
    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot(self):
        self.shooter.set_conveyor_speed(1)
        self.shooter.set_shooter_speed(0.8)
    
    @state
    def drive1(self, initial_call):
        if initial_call:
            self.drivetrain.reset_distance()
        self.drivetrain.set_speeds(0.8,0.8)
        if self.drivetrain.get_distance() > 70.0:
            self.next_state("drive2")
    
    @state
    def drive2(self):
        self.drivetrain.set_speeds(0,0)