
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
            self.eval_duration = 400
            self.current_score = 0
            self.best_score = -float("inf")
            self.parent_weights = self.random_weights()
            self.child_weights = None
            self.set_weights(self.parent_weights)
            self.phase = "evaluate_child"
            self.generation = 0
            self.scores_log = []

        translation, rotation = self.get_current_speed()
        self.current_score += translation * (1 - abs(rotation))
        self.iteration += 1

        if self.iteration % self.eval_duration == 0:
            if self.phase == "evaluate_child":
                child_score = self.current_score
                self.child_score = child_score

                if child_score > self.best_score:
                    self.best_score = child_score

                self.set_weights(self.parent_weights)
                self.phase = "evaluate_parent"
                self.current_score = 0
                self.reset()

            elif self.phase == "evaluate_parent":
                parent_score = self.current_score
                if self.child_score > parent_score:
                    self.parent_weights = self.child_weights
                    print(f"[{self.generation}] Replaced with better child: {self.child_score:.2f}")
                self.scores_log.append((self.generation, self.child_score, self.best_score))
                self.generation += 1

                self.child_weights = self.mutate(self.parent_weights)
                self.set_weights(self.child_weights)
                self.phase = "evaluate_child"
                self.current_score = 0
                self.reset()

    def random_weights(self):
        return [[random.choice([-1, 0, 1]) for _ in range(self.nb_sensors)] for _ in range(2)]

    def mutate(self, weights):
        i = random.randint(0, 1)
        j = random.randint(0, self.nb_sensors - 1)
        current = weights[i][j]
        new_vals = [-1, 0, 1]
        new_vals.remove(current)
        mutated = [row[:] for row in weights]
        mutated[i][j] = random.choice(new_vals)
        return mutated

    def reset(self):
        Robot.reset(self)
        self.robot_orientation = random.uniform(0, 2 * np.pi)
