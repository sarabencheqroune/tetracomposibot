
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Dumb"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self):
    # Senseurs
    robot_front = 1 - self.get_robot_sensor_value("sensor_front")
    robot_fl = 1 - self.get_robot_sensor_value("sensor_front_left")
    robot_fr = 1 - self.get_robot_sensor_value("sensor_front_right")
    wall_front = 1 - self.get_wall_sensor_value("sensor_front")
    wall_fl = 1 - self.get_wall_sensor_value("sensor_front_left")
    wall_fr = 1 - self.get_wall_sensor_value("sensor_front_right")

    # Comportement : aller tout droit
    t_straight = 1.0
    r_straight = 0.0

    # Comportement : éviter murs
    t_hateWall = 1.0 - 0.5 * (wall_front + wall_fl + wall_fr)
    r_hateWall = 1.5 * (wall_fr) - 1.5 * (wall_fl)

    # Comportement : aller vers robots
    t_loveBot = 0.5 + 0.5 * (robot_front + robot_fl + robot_fr)
    r_loveBot = 1.5 * (robot_fl) - 1.5 * (robot_fr)

    # Activation par priorité : loveBot > hateWall > straight
    weight_bot = robot_front + robot_fl + robot_fr
    weight_wall = wall_front + wall_fl + wall_fr

    total = weight_bot + weight_wall + 0.001  # évite div/0
    t = (t_loveBot * weight_bot + t_hateWall * weight_wall + t_straight * 0.001) / total
    r = (r_loveBot * weight_bot + r_hateWall * weight_wall + r_straight * 0.001) / total

    self.set_translation_value(t)
    self.set_rotation_value(r)

