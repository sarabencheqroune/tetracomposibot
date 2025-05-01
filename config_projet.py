# Configuration file (config_projet.py) pour Paint Wars

import arenas
import robot_challenger
import robot_champion

# === Paramètres généraux ===

display_mode = 0       # 0: normal ; 1: rapide ; 2: très rapide sans affichage
arena = 0              # numéro de l'arène (0–4)
position = False       # False: Challenger à gauche ; True: Challenger à droite
tmax = 500             # temps max de la simulation (en tours)
max_iterations = tmax

# === Affichage des stats ===
display_welcome_message = True
verbose_minimal_progress    = True
display_robot_stats         = False
display_team_stats          = True
display_tournament_results  = True
display_time_stats          = True

# === Mapping des comportements Challenger ===
# ID interne utilisé par robot_challenger pour définir le comportement
# Choix possibles : 0=optimized, 1=random, 2=subsumption
CHALLENGER_ID = 1
CHAMPION_ID   = 0

# === Répartition et instanciation des robots ===
def initialize_robots(arena_size=-1, particle_box=-1):
    robots = []
    # Centre vertical pour alignement
    y0 = arena_size // 2 - particle_box / 2
    # Abscisses de départ (bord gauche vs droite)
    margin = 4
    if not position:
        x_challenger = margin
        x_champion   = arena_size - margin - particle_box
        angle_ch      = 0   # challengers orientés Est
        angle_cp      = 180 # champions orientés Ouest
    else:
        x_challenger = arena_size - margin - particle_box
        x_champion   = margin
        angle_ch      = 180
        angle_cp      = 0
    # Équidistance verticale pour 4 robots
    offsets = [-30, -10, +10, +30]
    # Instanciation Challengers
    for i, dy in enumerate(offsets, start=1):
        bot = robot_challenger.Robot_player(
            x_challenger,
            y0 + dy,
            angle_ch,
            name=f"Challenger_{i}",
            team="Challengers"
        )
        # Forcer l'ID interne pour définir le comportement
        bot.robot_id = CHALLENGER_ID
        robots.append(bot)
    # Instanciation Champions
    for i, dy in enumerate(offsets, start=1):
        robots.append(
            robot_champion.Robot_player(
                x_champion,
                y0 + dy,
                angle_cp,
                name=f"Champion_{i}",
                team="Champions"
            )
        )
    return robots
