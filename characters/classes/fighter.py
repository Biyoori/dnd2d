from characters.classes.characterClass import CharacterClass

STARTING_SKILL_PROFICIENCY_OPTIONS = [
    "Acrobatics",
    "Animal Handling",
    "Athletics",
    "History",
    "Insight",
    "Intimidation",
    "Perception",
    "Survival"
]

class Fighter(CharacterClass):
    def __init__(self):
        super().__init__("Fighter", 10, ["Strength", "Constitution"], STARTING_SKILL_PROFICIENCY_OPTIONS, 2)