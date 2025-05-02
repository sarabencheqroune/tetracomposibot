# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiante : Sara Bencheqroune    21441027
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

team_name = "Red Dominators"
team_members = ["Sara Bencheqroune"]

import math
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
