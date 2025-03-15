class CharacterClass:
    def __init__(self, name: str, hitDie: int, savingThrowProficiencies: list[str], startingSkillProficiencyOptions: list[str], startingSkillProficiencies: int):
        self.name = name
        self.hitDie = hitDie
        self.savingThrowProficiencies = savingThrowProficiencies
        self.startingSkillProficiencyOptions = startingSkillProficiencyOptions
        self.startingSkillProficiencies = startingSkillProficiencies