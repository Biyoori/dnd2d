from core.settings import getColorFromPallette
from core.entity import Entity
from typing import Optional
from characters.classes.characterClass import CharacterClass
from characters.race import Race
from core.statsManager import StatsManager
from core.featLoader import getFeat
from inventory import Inventory
from item import Item

class Character(Entity):
    def __init__(
            self,
            x: Optional[int], 
            y: Optional[int], 
            cellSize: Optional[int], 
            name: str, 
            characterClasses: list[CharacterClass], 
            race: Race, 
            abilityScores: dict[str,int],
            skillProficiencies: list[str]
        ): 
        super().__init__(getColorFromPallette("red"), race.walkingSpeed)
        self.name = name
        self.race = race
        self.abilityScores = abilityScores
        self.skillProficiencies = skillProficiencies
        self.inventory = Inventory()

        # Character Classes
        self.primaryClass = characterClasses[0]
        self.characterClasses = {cls: 1 for cls in characterClasses}

        # Stats
        self.experience = 0      
        self.armorClass = 10
        self.proficiencyBonus = self.getProficiencyBonus()
        self.stats = StatsManager(
            self.abilityScores,
            self.proficiencyBonus,
            self.skillProficiencies,
            self.primaryClass.savingThrowProficiencies,
        )
        
        # Hit Points
        self.maxHP = self.calculateHP()
        self.currentHP = self.maxHP

        # Feats
        self.feats =  self.loadFeats()
        self.applyFeats()


    def calculateHP(self) -> int:
        return sum(cls.hitDie + self.stats.getAbilityMod("Constitution") for cls in self.characterClasses)
    
    def getProficiencyBonus(self) -> int:
        level = sum(lvl for lvl in self.characterClasses.values())
        return 2 + (level - 1) // 4
    
    def loadFeats(self) -> list:
        return [getFeat(feat) for feat in self.race.features]
    
    def applyFeats(self):
        for feat in self.feats:
            feat.apply(self)

    def pickUp(self, item: Item):
        self.inventory.addItem(item)

    def drop(self, itemName: str):
        self.inventory.removeItem(itemName)

    def displayCharacterInfo(self):
        print(f"{self.name}, {self.race.name}")
        print("Classes:", {cls.name: lvl for cls, lvl in self.characterClasses.items()})
        print("Skills:", self.skillProficiencies)