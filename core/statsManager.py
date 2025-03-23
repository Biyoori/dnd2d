import random
import re
from typing import Dict, List, Optional


class StatsManager:

    SKILLS = {
        "Acrobatics": "DEX",
    }

    SAVING_THROWS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

    def __init__(
        self, 
        abilityScores: Dict[str, int], 
        proficiencyBonus: Optional[int] = None, 
        skillProficiencies: Optional[List[str]] = None, 
        savingThrowProficiencies: Optional[list[str]] = None,
        fixedAttackBonus: Optional[int] = None,
        fixedDamageBonus: Optional[int] = None
    ):
        self.abilityScores = abilityScores
        self.proficiencyBonus = proficiencyBonus
        self.skillProficiencies = skillProficiencies
        self.savingThrowProficiencies = savingThrowProficiencies
        self.fixedAttackBonus = fixedAttackBonus
        self.fixedDamageBonus = fixedDamageBonus

    def getAbilityMod(self, ability: str):
        return (self.abilityScores[ability] - 10) // 2 
    
    def getAttackBonus(self, weapon = None):
        if self.fixedAttackBonus is not None:
            return self.fixedAttackBonus
        
        attribute = "STR" if weapon.weaponType == "melee" else "DEX"
        if weapon.finesse:
            attribute = "DEX" if self.getAbilityMod("DEX") > self.getAbilityMod("STR") else "STR"

        attackBonus = self.getAbilityMod(attribute)
        if weapon.name in self.skillProficiencies:
            attackBonus += self.proficiencyBonus
        return attackBonus
    
    def getDamageBonus(self, weapon = None):
        if self.fixedDamageBonus is not None:
            return self.fixedDamageBonus
        
        attribute = "STR" if weapon.weaponType == "melee" else "DEX"
        if weapon.finesse:
            attribute = "DEX" if self.getAbilityMod("DEX") > self.getAbilityMod("STR") else "STR"

        return self.getAbilityMod(attribute)

    def rollSkillCheck(self, skill: str):
        if skill not in self.SKILLS:
            raise ValueError(f"Unknown Skill: {skill}")
        
        ability = self.SKILLS[skill]
        abilityMod = self.getAbilityMod(ability)

        proficiencyBonus = self.proficiencyBonus if skill in self.skillProficiencies else 0
        roll = random.randint(1, 20)

        return roll, roll + proficiencyBonus + abilityMod
    
    def rollSavingThrow(self, ability: str):
        if ability not in self.SAVING_THROWS:
            raise ValueError(f"Unknown Ability: {ability}")
        
        abilityMod = self.getAbilityMod(ability)
        proficiencyBonus = self.proficiencyBonus if ability in self.savingThrowProficiencies else 0

        roll = random.randint(1, 20)

        return roll, roll + abilityMod + proficiencyBonus
    
    def rollDice(self, diceFormula: str) -> int:
        match = re.match(r"(\d+)d(\d+)([+-]\d+)", diceFormula)
        if not match:
            raise ValueError(f"Invalid dice formula: {diceFormula}")
        
        numDice = int(match.group(1))
        diceSides = int(match.group(2))
        modifier = int(match.group(3) or 0)

        diceRoll = sum(random.randint(1, diceSides) for _ in range(numDice))
        return diceRoll + modifier