# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiante : Sara Bencheqroune  
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

team_name = "Red Dominators"
team_members = ["Sara Bencheqroune"]

import mathfrom robot import *
import random
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "Sara"
    robot_id = -1
    memory = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if self.robot_id == 0:
            return self.braitenberg_advanced(sensors)
        elif self.robot_id == 1:
            return self.optimized_genetic(sensors)
        elif self.robot_id == 2:
            return self.memory_based(sensors)
        else:
            return self.my_strategy(sensors)

    # --- 1. Braitenberg amélioré ---
    def braitenberg_advanced(self, sensors):
        # Attraction vers les zones ouvertes + léger évitement obstacles
        rot = 0.8 * (sensors[sensor_front_left] - sensors[sensor_front_right])
        trans = 0.6 + 0.4 * min(sensors[sensor_front], sensors[sensor_front_left], sensors[sensor_front_right])
        noise = (random.random() - 0.5) * 0.05
        return trans, rot + noise, False

    # --- 2. Robot optimisé génétiquement ---
    def optimized_genetic(self, sensors):
        # Poids améliorés après test (ex : sélectionnés via TP2)
        weights_trans = [0.9, -0.4, 0.0, -0.2, 0.0, -0.4, -0.1, 0.9]
        weights_rot   = [-0.6, -1.0, -0.2, 0.0, 0.0, 0.2, 1.0, 0.6]
        translation = sum(s * w for s, w in zip(sensors, weights_trans))
        rotation = sum(s * w for s, w in zip(sensors, weights_rot))
        translation = max(min(translation, 1.0), 0.0)
        rotation = max(min(rotation, 1.0), -1.0)
        return translation, rotation, False

    # --- 3. Basé mémoire + capteurs ---
    def memory_based(self, sensors):
        # Alterne exploration / rotation selon environnement
        if sensors[sensor_front] < 0.3:
            self.memory = 1  # bloqué → tourne
        elif self.memory > 0:
            self.memory += 1
            if self.memory > 10:
                self.memory = 0  # reset après rotation
            return 0.2, 0.8, False

        return 0.9, 0.0, False

    # --- 4. Exploration intelligente ---
    def my_strategy(self, sensors):
        front = sensors[sensor_front]
        left = sensors[sensor_front_left]
        right = sensors[sensor_front_right]

        if front > 0.7:
            return 1.0, 0.0, False  # tout droit vite
        elif front < 0.2:
            # face bouchée → tourner vers le côté le plus libre
            rot = 0.9 if left > right else -0.9
            return 0.2, rot, False
        else:
            # petit ajustement de direction
            rot = 0.5 * (left - right)
            return 0.7, rot, False

import random

FORWARD_SPEED = 1.0
TURN_SPEED = 1.0

GENETIC_WEIGHTS = [(-1.2, -0.8, 0.0, 0.5, 0.8, 1.0, 0.6, -0.5),
                   (0.5, 1.0, 0.8, 0.6, -0.6, -1.0, -0.8, -0.5)]

def step(robotId, sensors):
    front = sensors[3]
    left = sensors[1]
    right = sensors[5]

    if robotId == 0:
        translation = FORWARD_SPEED
        rotation = 0.0
        for i in range(8):
            dist = sensors[i]
            weight = GENETIC_WEIGHTS[0][i]
            rotation += weight * (1.0 - dist)
        return translation, rotation

    if robotId == 1:
        translation = FORWARD_SPEED
        rotation = (right - left)
        if sensors[3] < 0.4:
            rotation += random.choice([-TURN_SPEED, TURN_SPEED])
        return translation, rotation

    if robotId == 2:
        if not hasattr(step, "memory"):
            step.memory = [0] * 4
        state = step.memory[robotId]

        if state < 50:
            translation = FORWARD_SPEED
            rotation = (right - left) * 0.5
        else:
            translation = 0.5
            rotation = -TURN_SPEED

        step.memory[robotId] = (state + 1) % 100
        return translation, rotation

    if front < 0.5:
        translation = 0.0
        rotation = TURN_SPEED if left > right else -TURN_SPEED
    else:
        translation = FORWARD_SPEED
        rotation = (right - left)
    return translation, rotation

class Robot_player:
    def __init__(self, x, y, angle, name, team):
        self.x = x
        self.y = y
        self.angle = angle
        self.theta = angle
        self.x0 = x
        self.y0 = y
        self.theta0 = angle
        self.name = name
        self.team = team
        self.robot_id = 0
        self.id = 0
        self.memory = 0
        self.log_sum_of_rotation = 0.0
        self.log_sum_of_translation = 0.0



    def step(self, sensor_values, sensor_view, sensor_robot, sensor_team):
        translation, rotation = step(self.robot_id, sensor_values)
        return translation, rotation, self.memory
