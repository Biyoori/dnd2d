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

class Fighter(CharacterClass):
    def __init__(self) -> None:
        super().__init__("Fighter", 10, ["Strength", "Constitution"], SKILL_PROFICIENCIES, 2, FEATS_BY_LEVEL)