from autochess.ac_data import ACData


def tftUnluckCalc(champion_tier: int, player_level: int, gold: int, champion_picked: int, others_picked: int,
                  is_dragon: bool, game_data: ACData):
    # Adjust gold for champion buying cost
    if is_dragon:
        gold_to_roll = gold - champion_tier * 2
    else:
        gold_to_roll = gold - champion_tier

    rolls = (gold_to_roll // 2) * 5

    # How many copies per champ exist in pool
    tier_pool_size = game_data.get_poolsize(champion_tier)

    # How many champions are in the tier
    tier_unit_amount = game_data.get_units_in_tier(champion_tier)

    amount_of_champs_in_pool_considered_hits = tier_pool_size - champion_picked
    amount_of_champs_in_pool_total = (tier_pool_size * tier_unit_amount) - champion_picked - others_picked

    # Level 7, Tier 5 -> 1%
    level_and_tier_probability = game_data.get_probability_of_level_and_tier(player_level, champion_tier)

    hit_chance_per_roll = level_and_tier_probability * (
            amount_of_champs_in_pool_considered_hits / amount_of_champs_in_pool_total
    )
    miss_chance_per_roll = 1 - hit_chance_per_roll

    miss_chance_total = miss_chance_per_roll ** rolls
    hit_chance_total = 1 - miss_chance_total

    return hit_chance_total
