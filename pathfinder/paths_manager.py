import os.path
import pickle
import pathfinder as pf

import paths


class PathsManager:

    FILE_NAME = os.path.join(os.path.dirname(__file__), "paths.pickle")

    paths = {}

    @classmethod
    def generate(cls, max_velocity=1.7, max_acceleration=2.0, max_jerk=60.0):
        cls.paths = {}
        for name, path in paths.PATHS.items():
            generated_path = []
            for trajectory in path:
                info, generated = pf.generate(
                    trajectory,
                    pf.FIT_HERMITE_CUBIC,
                    pf.SAMPLES_HIGH,
                    dt=0.02,
                    max_velocity=max_velocity,
                    max_acceleration=max_acceleration,
                    max_jerk=max_jerk)
                modifier = pf.modifiers.TankModifier(generated).modify(0.5)
                generated_path.append(modifier)
            cls.paths[name] = generated_path
        with open(cls.FILE_NAME, 'wb') as file:
            pickle.dump(cls.paths, file)

    @classmethod
    def load(cls):
        with open(cls.FILE_NAME, 'rb') as file:
            cls.paths = pickle.load(file)
