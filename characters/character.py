import pygame
from settings import getColorFromPallette
from core.entity import Entity
from typing import Optional
from characterClass import CharacterClass

class Character(Entity):
    def __init__(self, x: Optional[int], y: Optional[int], cellSize: Optional[int], name: str, characterClass: CharacterClass): #experience: int, #stats: Stats, inventory: Inventory, feats: list[Feat]
        super().__init__(x, y, cellSize, color=getColorFromPallette("red"))
        self.name = name
        self.characterClass = characterClass
        #self.experience = experience
        #self.stats = stats
        #self.inventory = inventory
        #self.feats = feats

    def __str__(self):
        return f"{self.name}: {self.characterClass.name}"