class CharacterClass:
    def __init__(self, name: str, hit_die: int, saving_throw_proficiencies: list[str], skill_proficiencies: list[str], skill_proficiency_points: int) -> None:
        self.name = name
        self.hit_die = hit_die
        self.saving_throws = saving_throw_proficiencies
        self.skill_proficiencies = skill_proficiencies
        self.skill_proficiency_points = skill_proficiency_points