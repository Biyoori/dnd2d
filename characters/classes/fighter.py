from characters.classes.barbarian import STARTING_GEAR
from characters.classes.characterClass import CharacterClass

SKILL_PROFICIENCIES = [
    "Acrobatics",
    "Animal Handling",
    "Athletics",
    "History",
    "Insight",
    "Intimidation",
    "Perception",
    "Survival"
]

FEATS_BY_LEVEL = {
    1: [],
    2: [],
    3: [],
    4: []
    #...
}

STARTING_GEAR = {
    "Weapons": [[("Longsword", 1), ("Shortsword", 2), ("Shield", 1)]],
    "Armor": [["Chain Mail", 1]],
    "Pack": [("Explorer's Pack", 1)],
}

class Fighter(CharacterClass):
    def __init__(self) -> None:
        super().__init__("Fighter", 10, ["Strength", "Constitution"], SKILL_PROFICIENCIES, 2, FEATS_BY_LEVEL, STARTING_GEAR)