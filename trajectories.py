import os.path
import pickle
import pathfinder as pf

trajectories = {}
generated_trajectories = {}

for name, trajectory in trajectories.items():
    info, generated = pf.generate(trajectory,
                                  pf.FIT_HERMITE_CUBIC,
                                  pf.SAMPLES_HIGH,
                                  dt=0.05,
                                  max_velocity=1.7,
                                  max_acceleration=2.0,
                                  max_jerk=60.0)
    modifier = pf.modifiers.TankModifier(generated).modify(0.5)
    generated_trajectories[name] = generated

file_name = os.path.join(os.path.dirname(__file__), "trajectories.pickle")
with open(file_name, 'wb') as file:
    pickle.dump(generated_trajectories, file)
