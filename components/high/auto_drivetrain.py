import pathfinder as pf
from pathfinder.followers import EncoderFollower
from navx import AHRS

import config
from components.low.drivetrain import Drivetrain
from pathfinder.paths_manager import PathsManager


class AutoDrivetrain:
    def __init__(self, drivetrain: Drivetrain, navx: AHRS):
        self.drivetrain = drivetrain
        self.navx = navx
        # Set default path
        self.path = PathsManager.paths["default"]
        # Set path position
        self.pos = 0
        # Set enabled
        self.enabled = False

    def set(self, pos):
        # Get trajectory
        self.trajectory = self.path[pos]
        # Get encoder followers
        self.left = EncoderFollower(self.trajectory.getLeftTrajectory())
        self.right = EncoderFollower(self.trajectory.getRightTrajectory())
        # Configure encoders
        self.left.configureEncoder(self.drivetrain.get_distance_left(), 1,
                                   0.0254)
        self.right.configureEncoder(self.drivetrain.get_distance_right(), 1,
                                    0.0254)
        # Set PIDVA values
        self.left.configurePIDVA(config.AutoDrivetrain.P_LEFT,
                                 config.AutoDrivetrain.I_LEFT,
                                 config.AutoDrivetrain.D_LEFT,
                                 1 / config.AutoDrivetrain.MAX_VELOCITY_LEFT,
                                 0)
        self.right.configurePIDVA(config.AutoDrivetrain.P_RIGHT,
                                  config.AutoDrivetrain.I_RIGHT,
                                  config.AutoDrivetrain.D_RIGHT,
                                  1 / config.AutoDrivetrain.MAX_VELOCITY_RIGHT,
                                  0)

    def next(self):
        if (self.pos + 1) < len(self.path):
            self.pos += 1
            self.set(self.pos)

    def set_path(self, name):
        self.path = PathsManager.paths[name]

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_finished(self):
        return self.left.isFinished() and self.right.isFinished()

    def execute(self):
        if self.enabled:
            angle_speed = -config.AutoDrivetrain.P_NAVX / 180 * pf.boundHalfDegrees(
                pf.r2d(self.left.getHeading()) - self.navx.getAngle() % 360)
            self.drivetrain.set_speeds(
                self.left.calculate(self.drivetrain.get_distance_left()) +
                angle_speed,
                self.right.calculate(self.drivetrain.get_distance_right()) -
                angle_speed)
