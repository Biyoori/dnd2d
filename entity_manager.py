from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from entities.enemy import Enemy
    from entities.character.character import Character

class GameEntityManager:
    def __init__(self) -> None:
        self._characters = []
        self._enemies = []

    def get_character(self) -> "Character":
        return self._characters[0] if self._characters else None
    
    def add_character(self, character: "Character"):
        self._characters.append(character)
    
    def get_enemies(self) -> List["Enemy"]:
        return self._enemies
    
    def add_enemy(self, enemy: "Enemy"):
        self._enemies.append(enemy)
    
    def remove_enemy(self, enemy: "Enemy"):
        if enemy in self._enemies:
            self._enemies.remove(enemy)