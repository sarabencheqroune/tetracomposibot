
from robot import * 
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()

    
from robot import * 
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()

    def step(self):
       if not hasattr(self, "iteration"):
            self.iteration = 0
            self.phase = "search"
            self.best_score = -float("inf")
            self.best_weights = None
            self.eval_index = 0
            self.eval_max = 500
            self.eval_duration = 400
            self.eval_subruns = 3
            self.subrun = 0
            self.current_score = 0
            self.partial_score = 0
            self.weights = self.random_weights()
            self.set_weights(self.weights)
            self.scores_log = []

        translation, rotation = self.get_current_speed()
        self.partial_score += translation * (1 - abs(rotation))
        self.iteration += 1

        # Fin d'un sous-test
        if self.iteration % self.eval_duration == 0 and self.phase == "search":
            self.current_score += self.partial_score
            self.partial_score = 0
            self.subrun += 1

            if self.subrun == self.eval_subruns:
                if self.current_score > self.best_score:
                    self.best_score = self.current_score
                    self.best_weights = self.weights
                    print(f"[{self.eval_index}] New best score: {self.best_score:.2f} → {self.weights}")
            
                self.scores_log.append((self.eval_index, self.current_score, self.best_score))
                self.eval_index += 1
    
                if self.eval_index >= self.eval_max:
                    self.phase = "exploit"
                    self.iteration = 0
                    self.set_weights(self.best_weights)
                    print(f"\n>>> Best strategy: {self.best_weights} (score={self.best_score})")
                else:
                    self.weights = self.random_weights()
                    self.set_weights(self.weights)
                self.subrun = 0
                self.current_score = 0

            self.reset()

        if self.phase == "exploit" and self.iteration % 1000 == 0:
            self.reset()
            self.set_weights(self.best_weights)

    def random_weights(self):
        return [[random.choice([-1, 0, 1]) for _ in range(self.nb_sensors)] for _ in range(2)]

    def reset(self):
        Robot.reset(self)
        self.robot_orientation = random.uniform(0, 2 * np.pi)
        self.robot_position = [random.uniform(0, self.world_width), random.uniform(0, self.world_height)]
