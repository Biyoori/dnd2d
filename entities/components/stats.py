from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, TYPE_CHECKING
import random
import re

from utils.utils import load_json

if TYPE_CHECKING:
    from items.weapon import Weapon
    from characters.classes.characterClass import CharacterClass

_CONFIG_PATH = "entities/character/stats_config.json"

@dataclass(frozen=True)
class AbilityScores:
    STR: int
    DEX: int
    CON: int
    INT: int
    WIS: int
    CHA: int

    def get_mod(self, ability: str) -> int:
        return (getattr(self, ability) - 10) // 2

@dataclass(frozen=True)
class Proficiencies:
    skills: List[str]
    saving_throws: List[str]

class StatsSystem:
    _config = load_json(_CONFIG_PATH)

    SKILLS: Dict[str, str] = _config.get("skills", {})
    SAVING_THROWS: List[str] = _config.get("saving_throws", [])

    def __init__(
        self,
        abilities: AbilityScores,
        proficiencies: Proficiencies,
        proficiency_bonus: int = 0,
    ) -> None:
        self._abilities = abilities
        self._proficiencies = proficiencies
        self.proficiency_bonus = proficiency_bonus

    def get_attack_bonus(self, weapon: "Weapon") -> int:
        bonus = self.determine_attack_attribute(weapon)

        if weapon.name in self._proficiencies.skills: #zmienić skills na weapon kiedy dodam listę.
            bonus += self.proficiency_bonus
        return bonus
    
    def get_damage_bonus(self, weapon: "Weapon") -> int:
        bonus = self.determine_attack_attribute(weapon)
        return bonus
    
    def determine_attack_attribute(self, weapon: "Weapon") -> int:
        if weapon.weapon_type == "melee" and not weapon.finesse:
            return self._abilities.get_mod("STR")
        return self._abilities.get_mod("DEX") if self._abilities.get_mod("DEX") > self._abilities.get_mod("STR") else self._abilities.get_mod("STR")

    def roll_skill_check(self, skill: str) -> tuple[int, int]:
        if skill not in self.SKILLS:
            raise ValueError(f"Unknown Skill: {skill}")
        
        ability = self.SKILLS[skill]
        ability_mod = self._abilities.get_mod(ability)

        proficiency_bonus = self.proficiency_bonus if skill in self._proficiencies.skills else 0
        roll = random.randint(1, 20)

        return roll, roll + proficiency_bonus + ability_mod   

    def roll_saving_throw(self, ability: str) -> tuple[int, int]:
        if ability not in self.SAVING_THROWS:
            raise ValueError(f"Unknown Ability: {ability}")
        
        ability_mod = self._abilities.get_mod(ability)
        proficiency_bonus = self.proficiency_bonus if ability in self._proficiencies.saving_throws else 0
        roll = random.randint(1, 20)

        return roll, roll + ability_mod + proficiency_bonus
    
    @staticmethod    
    def roll_dice(dice_formula: str) -> int:
        match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_formula)
        if not match:
            raise ValueError(f"Invalid dice formula: {dice_formula}")
        
        num_dice = int(match.group(1))
        dice_sides = int(match.group(2))
        modifier = int(match.group(3) or 0)

        dice_roll = sum(random.randint(1, dice_sides) for _ in range(num_dice))
        return dice_roll + modifier
    
    def get_mod(self, ability: str) -> int:
        return (getattr(self._abilities, ability) - 10) // 2
    
    def stats_increase_on_level_up(self, level: int, character_class: "CharacterClass", feats: List[str]):
        self.proficiency_bonus = 2 + (level - 1) // 4