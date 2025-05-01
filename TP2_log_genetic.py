import random
import numpy as np
import csv

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
            self.child_score = self.current_score
            if self.child_score > self.best_score:
                self.best_score = self.child_score

            self.set_weights(self.parent_weights)
            self.phase = "evaluate_parent"
            self.current_score = 0
            self.reset()

        elif self.phase == "evaluate_parent":
            if self.child_score > self.current_score:
                self.parent_weights = self.child_weights
                print(f"[{self.generation}] Child replaces parent: {self.child_score:.2f}")

            self.scores_log.append((self.generation, self.child_score, self.best_score))
            self.generation += 1

            if self.generation >= 500:
                print(f"Done. Best score: {self.best_score}")
                self.save_logs("log_genetic.csv")
                self.phase = "exploit"
                self.iteration = 0
                self.set_weights(self.parent_weights)
                return

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

def save_logs(self, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["generation", "score", "best_so_far"])
        for row in self.scores_log:
            writer.writerow(row)
