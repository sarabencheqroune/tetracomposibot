# Let's construct the new version of robot_challenger.py with 4 different strategies based on robot_id
# Projet "robotique" IA&Jeux 2025

from robot import *
import random
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "Sara"
    robot_id = -1
    memory = 0  # Unique memory slot (integer)

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Dispatch strategy based on robot_id
        if self.robot_id == 0:
            return self.braitenberg_advanced(sensors)
        elif self.robot_id == 1:
            return self.optimized_genetic(sensors)
        elif self.robot_id == 2:
            return self.memory_based(sensors)
        else:
            return self.my_custom_strategy(sensors)

    # -------------------------------
    # 1. Braitenberg advanced robot
    # -------------------------------
    def braitenberg_advanced(self, sensors):
        w_translation = 1.0 - sensors[sensor_front]
        w_rotation = sensors[sensor_front_left] - sensors[sensor_front_right]
        noise = (random.random() - 0.5) * 0.1
        return 1.0 - w_translation, w_rotation + noise, False

    # -------------------------------
    # 2. Genetic algorithm robot
    # (weights hardcoded from offline training)
    # -------------------------------
    def optimized_genetic(self, sensors):
        weights_trans = [0.8, -0.3, 0.1, -0.1, 0.1, -0.3, 0.2, 0.8]
        weights_rot = [-0.5, -0.8, -0.2, -0.1, 0.1, 0.2, 0.8, 0.5]
        translation = sum([s * w for s, w in zip(sensors, weights_trans)])
        rotation = sum([s * w for s, w in zip(sensors, weights_rot)])
        return max(min(translation, 1.0), -1.0), max(min(rotation, 1.0), -1.0), False

    # -------------------------------
    # 3. Memory-based strategy
    # -------------------------------
    def memory_based(self, sensors):
        if self.memory % 20 < 10:
            translation = 0.8
            rotation = 0.2
        else:
            translation = 0.6
            rotation = -0.5
        self.memory += 1
        return translation, rotation, False

    # -------------------------------
    # 4. Custom exploration strategy
    # -------------------------------
    def my_custom_strategy(self, sensors):
        front_clear = sensors[sensor_front] > 0.6
        if front_clear:
            translation = 1.0
            rotation = 0.0
        else:
            translation = 0.0
            rotation = 0.8 if sensors[sensor_front_left] > sensors[sensor_front_right] else -0.8
        return translation, rotation, False
