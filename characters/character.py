from settings import getColorFromPallette
from core.entity import Entity
from typing import Optional
from characterClass import CharacterClass
from race import Race


class Character(Entity):
    def __init__(
            self, x: Optional[int], 
            y: Optional[int], 
            cellSize: Optional[int], 
            name: str, 
            characterClass: CharacterClass, 
            race: Race, 
            abilityScores: dict[str,int], 
        ): #experience: int, #stats: Stats, inventory: Inventory, 

        super().__init__(x, y, cellSize, color=getColorFromPallette("red"))
        self.name = name
        self.characterClass = characterClass
        self.race = race
        self.abilityScores = abilityScores
         #self.experience = experience
        #self.stats = stats
        #self.inventory = inventory
        self.feats = self.race.features

    def __str__(self):
        return f"{self.name}: {self.characterClass.name}"