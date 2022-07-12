from autochess.ac_data import ACData


class ACJson:
    def __init__(self, game_data: ACData):
        self.game_data = game_data

    # data = { 'Yasuo': 1, 'Yasuo-taken': 3 }
    # splits data into two dicts like
    # desired_champs = { 'Yasuo': 1 }
    # taken_champs = { 'Yasuo': 3 }
    def seperate_data(self, data: dict):
        desired_champs = {}
        taken_champs = {}

        for champ, amount in data.items():
            if champ in self.game_data.all_champs:
                desired_champs[champ] = amount
            elif champ[:-6] in self.game_data.all_champs:
                taken_champs[champ[:-6]] = amount

        return desired_champs, taken_champs

    def desired_champs_from_json(self, data: dict) -> dict:
        desired_champs = self.create_dict_champ_zero()

        for champ, amount in data.items():
            for tier in ["1", "2", "3", "4", "5"]:
                if champ in desired_champs[tier]:
                    desired_champs[tier][champ] = int(amount)
                    break

        self.create_sum_field_for_dict(desired_champs)
        return desired_champs

    def champ_pool_from_json(self, data) -> dict:
        champ_pool = self.create_dict_champ_poolsize()

        for champ, amount in data.items():
            for tier in ["1", "2", "3", "4", "5"]:
                if champ in champ_pool[tier]:
                    champ_pool[tier][champ] = champ_pool[tier][champ] - int(amount)
                    break

        self.create_sum_field_for_dict(champ_pool)
        return champ_pool

    def create_dict_champ_zero(self) -> dict:
        board = {}

        for tier in ["1", "2", "3", "4", "5"]:
            board[tier] = {}
            for champ in self.game_data.get_champs_of_tier(int(tier)):
                board[tier][champ] = 0

        return board

    def create_dict_champ_poolsize(self) -> dict:
        board = {}

        for tier in ["1", "2", "3", "4", "5"]:
            board[tier] = {}
            for champ in self.game_data.get_champs_of_tier(int(tier)):
                board[tier][champ] = self.game_data.get_poolsize(int(tier))

        return board

    def create_sum_field_for_dict(self, board: dict):
        board["sum"] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}

        for tier in ["1", "2", "3", "4", "5"]:
            for champ in self.game_data.get_champs_of_tier(int(tier)):
                board["sum"][tier] = board["sum"][tier] + board[tier][champ]
