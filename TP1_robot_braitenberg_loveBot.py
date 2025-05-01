
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

    ddef step(self):
    front = 1 - self.get_robot_sensor_value("sensor_front")
    fl = 1 - self.get_robot_sensor_value("sensor_front_left")
    fr = 1 - self.get_robot_sensor_value("sensor_front_right")

    translation = 0.5 + 0.5 * (front + fl + fr)
    rotation = 1.5 * (fl) - 1.5 * (fr)

    self.set_translation_value(translation)
    self.set_rotation_value(rotation)

