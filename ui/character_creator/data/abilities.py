ABILITY_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

def create_default_scores() -> dict[str, int]:
    return {name: 8 for name in ABILITY_NAMES}