from copy import deepcopy

from autochess.ac_simulation import ACSimulation
from autochess.ac_data import ACData


class ACSimulationAnalyzer:
    def __init__(self, n: int, player_level: int, gold: int, desired_champ_pool: dict, starting_champ_pool: dict,
                 game_data: ACData):
        self.n = n
        self.gold = gold
        self.player_level = player_level
        self.game_data = game_data

        self.desired_champ_pool = desired_champ_pool
        self.starting_champ_pool = starting_champ_pool

        self.hits = 0

    def analyze(self):
        for _ in range(self.n):
            hit_everything = ACSimulation(player_level=self.player_level,
                                          gold=self.gold,
                                          starting_champ_pool=deepcopy(self.starting_champ_pool),
                                          desired_champ_pool=deepcopy(self.desired_champ_pool),
                                          game_data=self.game_data
                                          ).start()
            if hit_everything:
                self.hits += 1

        return self.hits / self.n
