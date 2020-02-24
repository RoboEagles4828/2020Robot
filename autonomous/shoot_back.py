from robotpy_ext.autonomous import StatefulAutonomous
from robotpy_ext.autonomous.stateful_autonomous import state
from robotpy_ext.autonomous.stateful_autonomous import timed_state
import navx
from autonomous import Autonomous
from components.low.shooter import Shooter
from components.low.drivetrain import Drivetrain
import config
class ShootBack(StatefulAutonomous):
    autonomous: Autonomous
    shooter: Shooter
    drivetrain: Drivetrain
    navx: navx

    MODE_NAME = "Shoot 3 Go Back"
    
    @timed_state(duration=3.0, next_state="drive1", first=True)
    def shoot(self):
        self.autonomous.shoot()
    
    @state
    def drive1(self, initial_call):
        self.shooter.set_conveyor_speed(0)
        self.shooter.set_shooter_speed(0)
        if self.autonomous.drive(initial_call, -config.Autonomous.DRIVE_DISTANCE):
            self.next_state("end")
    
    @state
    def end(self):
        self.drivetrain.set_speeds(0,0)
        self.done()