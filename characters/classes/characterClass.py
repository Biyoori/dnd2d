from typing import Dict, List

class CharacterClass:
    def __init__(
        self, 
        name: str, 
        hit_die: int, 
        saving_throw_proficiencies: List[str], 
        skill_proficiencies: List[str], 
        skill_proficiency_points: int, 
        feats_by_level: Dict[int, List[str]],
        starting_gear: Dict[str, List[str]],
    ) -> None:
        
        self.name = name
        self.hit_die = hit_die
        self.saving_throws = saving_throw_proficiencies
        self.skill_proficiencies = skill_proficiencies
        self.skill_proficiency_points = skill_proficiency_points
        self.feats_by_level = feats_by_level
        self.starting_gear = starting_gear
        
    def get_feats_for_level(self, level: int) -> List[str]:
        return self.feats_by_level.get(level, [])