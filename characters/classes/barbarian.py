from characters.classes.characterClass import CharacterClass

STARTING_SKILL_PROFICIENCY_OPTIONS = [
    "Animal Handling",
    "Athletics",
    "Intimidation",
    "Nature",
    "Perception",
    "Survival"
]

class Barbarian(CharacterClass):
    def __init__(self):
        super().__init__("Barbarian", 12, ["Strength", "Constitution"], STARTING_SKILL_PROFICIENCY_OPTIONS, 2)