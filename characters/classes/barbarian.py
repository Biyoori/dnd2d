from characters.classes.characterClass import CharacterClass

SKILL_PROFICIENCIES = [
    "Animal Handling",
    "Athletics",
    "Intimidation",
    "Nature",
    "Perception",
    "Survival"
]

class Barbarian(CharacterClass):
    def __init__(self) -> None:
        super().__init__("Barbarian", 12, ["Strength", "Constitution"], SKILL_PROFICIENCIES, 2)