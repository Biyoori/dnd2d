import random

class StatsManager:

    SKILLS = {
        "Acrobatics": "Dexterity",
    }

    SAVING_THROWS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    def __init__(self, abilityScores: dict[str, int], proficiencyBonus: int, skillProficiencies: list[str], savingThrowProficiencies: list[str]):
        self.abilityScores = abilityScores
        self.proficiencyBonus = proficiencyBonus
        self.skillProficiencies = skillProficiencies
        self.savingThrowProficiencies = savingThrowProficiencies

    def getAbilityMod(self, ability: str):
        return (self.abilityScores[ability] - 10) // 2 
    
    def getAttackBonus(self, weapon):
        attribute = "Strength" if weapon.weaponType == "melee" else "Dexterity"
        if weapon.finesse:
            attribute = "Dexterity" if self.getAbilityMod("Dexterity") > self.getAbilityMod("Strength") else "Strength"

        attackBonus = self.getAbilityMod(attribute)
        if weapon.name in self.skillProficiencies:
            attackBonus += self.proficiencyBonus
        return attackBonus
    
    def getDamageBonus(self, weapon):
        attribute = "Strength" if weapon.weaponType == "melee" else "Dexterity"
        if weapon.finesse:
            attribute = "Dexterity" if self.getAbilityMod("Dexterity") > self.getAbilityMod("Strength") else "Strength"

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
