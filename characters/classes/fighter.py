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

class Fighter(CharacterClass):
    def __init__(self) -> None:
        super().__init__("Fighter", 10, ["Strength", "Constitution"], SKILL_PROFICIENCIES, 2)