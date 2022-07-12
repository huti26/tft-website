import configparser
import ast
from pathlib import Path


def pretty_output_chance_list_value(value: float) -> str:
    value = value * 100
    value = f'{value:3.0f}%'.strip()
    return value


class ACData:
    def __init__(self, game: str):
        config = configparser.ConfigParser()
        config_path = (Path(__file__).parent.absolute() / "data.ini").resolve()
        config.read(str(config_path))

        self.common = ast.literal_eval(config.get(game, "common"))
        self.uncommon = ast.literal_eval(config.get(game, "uncommon"))
        self.rare = ast.literal_eval(config.get(game, "rare"))
        self.epic = ast.literal_eval(config.get(game, "epic"))
        self.legendary = ast.literal_eval(config.get(game, "legendary"))

        self.dragons = ast.literal_eval(config.get(game, "dragons"))

        # sort for now
        self.common = sorted(self.common)
        self.uncommon = sorted(self.uncommon)
        self.rare = sorted(self.rare)
        self.epic = sorted(self.epic)
        self.legendary = sorted(self.legendary)

        self.all_lists = [self.common, self.uncommon, self.rare, self.epic, self.legendary]
        self.all_lists_labels = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        self.all_lists_and_labels = list(zip(self.all_lists, self.all_lists_labels))

        self.all_champs = self.common + self.uncommon + self.rare + self.epic + self.legendary

        self.poolsizes = ast.literal_eval(config.get(game, "poolsizes"))
        self.amount_of_champs_per_tier = ast.literal_eval(config.get(game, "units_in_tier"))
        self.chances = ast.literal_eval(config.get(game, "chances"))
        self.max_player_level = ast.literal_eval(config.get(game, "max_player_level"))
        self.game_name = config.get(game, "game_name")
        self.patch = config.get(game, "patch")

        # self.chances_pretty = map(pretty_output_chance_list_value, self.chances)
        self.chances_pretty = [[pretty_output_chance_list_value(chance) for chance in row] for row in self.chances]

        self.champion_costs = {}
        for tier, champ_list in enumerate(self.all_lists):
            for champ in champ_list:
                if champ in self.dragons:
                    self.champion_costs[champ] = (tier + 1) * 2
                else:
                    self.champion_costs[champ] = tier + 1

    # Conversion from starting at 0 to starting at 1
    def get_champs_of_tier(self, tier: int):
        return self.all_lists[tier - 1]

    # Conversion from starting at 0 to starting at 1
    def get_poolsize(self, tier: int):
        return self.poolsizes[tier - 1]

    # Conversion from starting at 0 to starting at 1
    def get_probabilities_of_level(self, player_level: int) -> list:
        # chances[2][1] = chance to roll t2 unit on level 3 = 0.25
        return self.chances[player_level - 1]

    # Conversion from starting at 0 to starting at 1
    def get_probability_of_level_and_tier(self, player_level: int, tier: int) -> list:
        # chances[2][1] = chance to roll t2 unit on level 3 = 0.25
        return self.chances[player_level - 1][tier - 1]

    # Conversion from starting at 0 to starting at 1
    def get_units_in_tier(self, tier: int):
        return self.amount_of_champs_per_tier[tier - 1]

    def is_dragon(self, champion_name):
        return champion_name in self.dragons
