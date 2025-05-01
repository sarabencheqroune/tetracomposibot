
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
    front = self.get_sensor_value("sensor_front")
    front_left = self.get_sensor_value("sensor_front_left")
    front_right = self.get_sensor_value("sensor_front_right")
    back_left = self.get_sensor_value("sensor_back_left")
    back_right = self.get_sensor_value("sensor_back_right")

    # Inversion des distances (1=loin → 0; 0=proche → 1)
    inv_front = 1 - front
    inv_fl = 1 - front_left
    inv_fr = 1 - front_right
    inv_bl = 1 - back_left
    inv_br = 1 - back_right

    # Vitesses proportionnelles aux senseurs
    translation = 1.0 - 0.5 * (inv_front + inv_fl + inv_fr)
    rotation = 1.5 * (inv_fr + inv_br) - 1.5 * (inv_fl + inv_bl)

    self.set_translation_value(translation)
    self.set_rotation_value(rotation)

