# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiante : Sara Bencheqroune    21441027
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import *
import random
import numpy as np

class Robot_player(Robot):
    # Nom de votre équipe
    team_name = "WarriorForce"

    def __init__(self, x, y, orientation, name="", team="A"):
        # Appel du constructeur de base (position initiale, orientation, nom, équipe)
        super().__init__(x, y, orientation, name=name, team=team)
        # Mémoire unique (entier) initialisée à 0
        self.memory = 0

    def step(self, sensor_values, sensor_view, sensor_robot, sensor_team):
        """
        sensor_values : liste de distances (float) pour chaque capteur
        sensor_view   : non utilisé
        sensor_robot  : liste d'identifiants de robot détectés (int ou -1)
        sensor_team   : liste de codes équipe des robots détectés (int ou -1)
        Retourne : (translation:float, rotation:float, ask_for_reset:bool)
        """
        # Extraction des distances et nombre de capteurs
        distance_data = sensor_values
        nb_sensors = len(distance_data)

        # Séparer murs et robots
        distances_wall = np.array([
            distance_data[i] if (sensor_robot[i] == -1 and sensor_team[i] == -1) else 1.0
            for i in range(nb_sensors)
        ])
        distances_robot = np.array([
            distance_data[i] if sensor_robot[i] != -1 else 1.0
            for i in range(nb_sensors)
        ])
        inv_wall = 1 - distances_wall
        inv_robot = 1 - distances_robot

        # Comportements de base
        def hate_wall():
            t = 1.0 - 0.5 * np.mean(inv_wall[:3])
            r = 2.0 * (inv_wall[2] - inv_wall[1])
            return t, r

        def random_walker():
            mem = self.memory
            if mem == 0:
                # Init angle aléatoire
                angle = random.uniform(-1, 1)
                mem = int(angle * 1000)
            t = 1.0
            r = mem / 1000.0
            # Rebond sur mur si trop proche
            if np.mean(inv_wall[:3]) > 0.8:
                mem = 0
            self.memory = mem
            return t, r

        def optimized_behavior():
            # Poids issus d'une optimisation génétique préalable
            weights = [[-1, 1, -1, 0, 1], [1, -1, 1, 0, -1]]
            t = sum(weights[0][i] * (1 - distance_data[i]) for i in range(nb_sensors))
            r = sum(weights[1][i] * (1 - distance_data[i]) for i in range(nb_sensors))
            # Clamp
            t = max(0.0, min(1.0, t))
            r = max(-1.0, min(1.0, r))
            return t, r

        # Sélection du comportement selon l'identifiant du robot
        rid = self.robot_id
        if rid == 0:
            t, r = optimized_behavior()
        elif rid == 1:
            t, r = random_walker()
        elif rid in [2, 3]:
            t_wall, r_wall = hate_wall()
            t_rand, r_rand = random_walker()
            # Subsomption : priorité évitement de murs si obstacle
            if np.mean(inv_wall[:3]) > 0.3:
                t, r = t_wall, r_wall
            else:
                t, r = t_rand, r_rand
        else:
            # Comportement par défaut : random walk
            t, r = random_walker()

        # Pas de réinitialisation demandée
        return t, r, False
