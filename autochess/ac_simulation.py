from autochess.ac_data import ACData
import random


# custom choice algorithm, because numpy performance is bad on single rolls(?)
def choice(options: list, probs: list, n: int) -> list:
    choices = []

    for _ in range(n):
        x = random.random()
        cum = 0
        i = 0
        for p in probs:
            cum += p
            if x < cum:
                break
            i = i + 1

        # precision error
        if i == len(options):
            i = i - 1

        choices.append(options[i])

    return choices


class ACSimulation:
    def __init__(self, player_level: int, gold: int, starting_champ_pool: dict, desired_champ_pool: dict,
                 game_data: ACData):
        self.champ_pool = starting_champ_pool
        self.desired_champ_pool = desired_champ_pool
        self.player_level: int = player_level
        self.gold: int = gold
        self.game_data = game_data

        self.champs_to_hit_count = 0
        for tier in range(1, 6):
            self.champs_to_hit_count += self.desired_champ_pool["sum"][str(tier)]

    def simulate_champs_rolled(self):
        # rerolling costs 2 gold & gives your 5 rolls
        # buying a unit costs at least 1
        while self.gold >= 3 and self.champs_to_hit_count > 0:
            self.gold -= 2

            for _ in range(5):
                # roll a tier
                tier = choice(
                    options=["1", "2", "3", "4", "5"],
                    probs=self.game_data.get_probabilities_of_level(self.player_level), n=1
                )[0]

                # roll a champ in rolled tier
                champ_names = list(self.champ_pool[tier].keys())
                poolsizes = list(self.champ_pool[tier].values())

                probabilites = [poolsize / self.champ_pool["sum"][tier] for poolsize in poolsizes]

                rolled_champ = choice(options=champ_names, probs=probabilites, n=1)[0]
                rolled_champ_cost = self.game_data.champion_costs[rolled_champ]

                # buy it?
                if self.desired_champ_pool[tier][rolled_champ] > 0 and self.gold >= rolled_champ_cost:
                    self.gold -= rolled_champ_cost

                    self.desired_champ_pool[tier][rolled_champ] -= 1
                    self.desired_champ_pool["sum"][tier] -= 1

                    self.champ_pool[tier][rolled_champ] -= 1
                    self.champ_pool["sum"][tier] -= 1

                    self.champs_to_hit_count -= 1

    # code keeps track of sums per tier for the desired_champ_pool
    # if any of those values is > 0, we did not hit all desired champs
    def create_output(self):
        hit_everything = True
        for tier in ["1", "2", "3", "4", "5"]:
            if self.desired_champ_pool["sum"][tier] > 0:
                hit_everything = False

        return hit_everything

    def start(self):
        self.simulate_champs_rolled()
        return self.create_output()
