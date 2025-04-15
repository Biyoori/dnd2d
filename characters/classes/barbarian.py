from tkinter import W
from characters.classes.characterClass import CharacterClass

SKILL_PROFICIENCIES = [
    "Animal Handling",
    "Athletics",
    "Intimidation",
    "Nature",
    "Perception",
    "Survival"
]

FEATS_BY_LEVEL = {
    1: ["Rage", "Unarmored_defense"],
    2: ["Danger Sense", "Reckless Attack"],
    3: ["Primal Knowledge"],
    4: []
    #...
}

STARTING_GEAR = {
    "Weapons": [[("Greataxe", 1), ("Handaxe", 4)]],
    "Pack": [("Explorer's Pack", 1)],
}

class Barbarian(CharacterClass):
    def __init__(self) -> None:
        super().__init__("Barbarian", 12, ["Strength", "Constitution"], SKILL_PROFICIENCIES, 2, FEATS_BY_LEVEL, STARTING_GEAR)