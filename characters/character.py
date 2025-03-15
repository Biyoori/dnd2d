from core.settings import getColorFromPallette
from core.entity import Entity
from typing import Optional
from characters.classes.characterClass import CharacterClass
from characters.race import Race
from core.statsManager import StatsManager
from core.featLoader import getFeat


class Character(Entity):
    def __init__(
            self, x: Optional[int], 
            y: Optional[int], 
            cellSize: Optional[int], 
            name: str, 
            characterClasses: list[CharacterClass], 
            race: Race, 
            abilityScores: dict[str,int],
            skillProficiencies: list[str]
        ): #inventory: Inventory

        super().__init__(x, y, cellSize, color=getColorFromPallette("red"))
        self.name = name
        self.primaryClass = characterClasses[0]
        self.characterClasses = {cls: 1 for cls in characterClasses}
        self.race = race
        self.abilityScores = abilityScores
        self.experience = 0
        self.proficiencyBonus = self.getProficiencyBonus()
        self.armorClass = 10
        #self.inventory = inventory
        self.feats = [getFeat(feat) for feat in self.race.features]
        for feat in self.feats:
            feat.apply(self)

        self.skillProficiencies = skillProficiencies

        self.stats = StatsManager(
            self.abilityScores,
            self.proficiencyBonus,
            self.skillProficiencies,
            self.primaryClass.savingThrowProficiencies,
        )

        self.maxHP = self.calculateHP()
        self.currentHP = self.maxHP
    
    def calculateHP(self):
        return sum(cls.hitDie + self.stats.getAbilityMod("Constitution") for cls in self.characterClasses)
    
    def getProficiencyBonus(self):
        level = sum(lvl for lvl in self.characterClasses.values())
        return 2 + (level - 1) // 4

    def displayCharacterInfo(self):
        print(f"{self.name}, {self.race.name}")
        print("Classes:", {cls.name: lvl for cls, lvl in self.characterClasses.items()})
        print("Skills:", self.skillProficiencies)