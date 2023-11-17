import random
import threading
import time
from collections import defaultdict
from icecream import ic  # Importing ic for logging


def create_gem_finder(chance):
    def find_gem(simp):
        found = random.randint(1, 10) <= chance
        #ic(simp.name, "found a gem:")  # Logging with ic
        return 1 if found else 0
    return find_gem


class Simp(threading.Thread):
    def __init__(self, name, environments, leaderboard, lock, winner_flag):
        super().__init__()
        self.name = name
        self.gems = 0
        self.environments = environments
        self.leaderboard = leaderboard
        self.lock = lock
        self.winner_flag = winner_flag

    def run(self):
        while self.gems < 10 and not self.winner_flag.is_set():
            gem_finder = random.choice(self.environments)
            self.gems += gem_finder(self)
            with self.lock:
                self.leaderboard[self.name] = self.gems
                if self.gems >= 10:
                    self.winner_flag.set()
                    ic(self.name, "wins with", self.gems, "gems")  # Adjusted logging
                    break


if __name__ == '__main__':
    environments = [create_gem_finder(chance) for chance in [3, 2, 1, 4]]
    leaderboard = defaultdict(int)
    lock = threading.Lock()
    winner_flag = threading.Event()
    simps = [Simp(f"Simp{i}", environments, leaderboard, lock, winner_flag) for i in range(1, 16)]

    for simp in simps:
        time.sleep(random.uniform(0, 0.5))  # Random delay before starting each thread
        simp.start()

    for simp in simps:
        simp.join()