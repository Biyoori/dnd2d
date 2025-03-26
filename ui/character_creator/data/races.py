from characters.races.race import Race
from utils.utils import load_json

RACES_DATA = load_json("characters/races/races.json")

def get_races() -> list[Race]:
    return [Race(race, data) for race, data in RACES_DATA.items()]

def get_race(name: str) -> Race:
    return Race(name, RACES_DATA[name])

