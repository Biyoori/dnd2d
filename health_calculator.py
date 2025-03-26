from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.classes.characterClass import CharacterClass
    from entities.components.stats import StatsSystem


class HealthCalculator:
    @staticmethod
    def calc_character(character_classes: list["CharacterClass"], stats: "StatsSystem") -> int:
        base_hp = sum(cls.hit_die for cls in character_classes)
        con_mod = stats._abilities.get_mod("CON")
        return base_hp + con_mod
    
    @staticmethod
    def calc_enemy(hit_points_data) -> int:
        if "fixed" in hit_points_data:
            return hit_points_data["fixed"]
        elif "formula" in hit_points_data:
            return #roll for health
        else:
            raise ValueError("No valid hit points data provided.")