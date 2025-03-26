from typing import Dict, Any

class Race:
    def __init__(self, name: str, race_data: Dict[str, Any]) -> None:
        self.name = name
        self.creature_type = race_data["creature_type"]
        self.size = race_data["size"]
        self.walking_speed = race_data["speed"]
        self.flying_speed = 0
        self.ability_score_bonuses = race_data["ability_score_bonuses"]
        self.features = race_data["features"]

    def apply_ability_bonuses(self, base_stats: Dict[str, int]) -> Dict[str, int]:
        new_stats = base_stats.copy()
        for stat, bonus in self.ability_score_bonuses.items():
            new_stats[stat] += bonus
        return new_stats

    def __str__(self) -> str:
        return f"{self.name} ({self.creature_type}, {self.size}) - Speed: {self.walking_speed}, Flying Speed: {self.flying_speed}, Traits: {', '.join(self.features)}"