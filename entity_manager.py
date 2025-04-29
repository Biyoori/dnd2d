from typing import TYPE_CHECKING, List
from debugging import logger
from entities.lootable import Lootable

from core.event import Event

if TYPE_CHECKING:
    from entities.enemy import Enemy
    from entities.character.character import Character

class GameEntityManager:
    def __init__(self) -> None:
        self._characters = []
        self._enemies = []
        self._loot = []

        Event.subscribe("remove_enemy", self.remove_enemy)

        Event.subscribe("add_lootable", self.add_loot)
        Event.subscribe("remove_lootable", self.remove_loot)

    def get_character(self) -> "Character":
        return self._characters[0] if self._characters else None
    
    def add_character(self, character: "Character") -> None:
        self._characters.append(character)
    
    def get_enemies(self) -> List["Enemy"]:
        return self._enemies
    
    def add_enemy(self, enemy: "Enemy") -> None:
        self._enemies.append(enemy)

    def add_loot(self, loot: "Lootable") -> None:
        self._loot.append(loot)
        logger.log(f"Added loot: {loot}", "DEBUG")
        
    def get_loot(self) -> List["Lootable"]:
        return self._loot
    
    def remove_loot(self, loot: "Lootable") -> None:
        if loot in self._loot:
            logger.log(f"Removing loot: {loot}", "DEBUG")
            self._loot.remove(loot)
        else:
            logger.log(f"Loot not found: {loot}", "ERROR")
    
    def remove_enemy(self, enemy: "Enemy") -> None:
        if enemy in self._enemies:
            logger.log(f"Removing enemy: {enemy}", "DEBUG")
            Event.notify("remove_combatant", enemy)
            self._enemies.remove(enemy)
            del enemy
            
