import random
import numpy as np
import csv

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
                self.save_logs("log_randomsearch2.csv")
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

def save_logs(self, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["evaluation", "score", "best_so_far"])
        for line in self.scores_log:
            writer.writerow(line)
