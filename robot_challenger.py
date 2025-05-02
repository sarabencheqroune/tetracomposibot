# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiante : Sara Bencheqroune    21441027
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

team_name = "Red Dominators"
team_members = ["A","B","C","D"]

import math
import random

# Vitesses de base
FORWARD_SPEED = 1.0
TURN_SPEED = 1.0

# Poids génétiquement optimisés (exemple)
GENETIC_WEIGHTS = [(-1.2, -0.8, 0.0, 0.5, 0.8, 1.0, 0.6, -0.5),
                   (0.5, 1.0, 0.8, 0.6, -0.6, -1.0, -0.8, -0.5)]

def step(robotId, sensors):
    # Initialisation
    front = sensors[3][0]
    left = sensors[1][0]
    right = sensors[5][0]

    # --- Architecture de subsomption ---

    # Niveau 3 : Robot spécialisé  -> Comportement optimisé
    if robotId == 0:
        translation = FORWARD_SPEED
        rotation = 0.0
        for i in range(8):
            dist = sensors[i][0]
            weight = GENETIC_WEIGHTS[0][i]
            rotation += weight * (1.0 - dist)  # Plus proche = plus d'effet
        return translation, rotation

    # Niveau 2 : Robot explorateur (ex: robot 1) -> Comportement Braitenberg attraction vers zones libres
    if robotId == 1:
        translation = FORWARD_SPEED
        rotation = (right - left)
        if sensors[3][0] < 0.4:
            rotation += random.choice([-TURN_SPEED, TURN_SPEED])
        return translation, rotation

    # Niveau 1 : Robot patrouilleur (ex: robot 2) -> Alterne exploration/fuite
    if robotId == 2:
        if not hasattr(step, "memory"):
            step.memory = [0] * 4
        state = step.memory[robotId]

        # Comportement basé sur mémoire : alterne toutes les 50 steps
        if state < 50:
            translation = FORWARD_SPEED
            rotation = (right - left) * 0.5
        else:
            translation = 0.5
            rotation = -TURN_SPEED

        step.memory[robotId] = (state + 1) % 100
        return translation, rotation

    # Niveau 0 : Robot par défaut (ex: robot 3) -> Évitement simple
    if front < 0.5:
        translation = 0.0
        rotation = TURN_SPEED if left > right else -TURN_SPEED
    else:
        translation = FORWARD_SPEED
        rotation = (right - left)
    return translation, rotation
