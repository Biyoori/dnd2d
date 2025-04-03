from typing import TYPE_CHECKING, List
from enum import Enum

if TYPE_CHECKING:
    from entities.entity import Entity

class Faction(Enum):
    PLAYER = 1
    ENEMY = 2
    NEUTRAL = 3

class FactionSystem:
    def __init__(self) -> None:
        self._enemy_relations = {Faction.PLAYER: Faction.ENEMY}

    def get_enemies(self, entities: List["Entity"], for_faction: Faction):
        enemies = set()
        for entity in entities:
            if entity.faction is self._enemy_relations.get(for_faction, set()):
                enemies.add(entity)
        return list(enemies)