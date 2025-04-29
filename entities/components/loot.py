from dataclasses import dataclass
from typing import Tuple

from core.event import Event
from entities.lootable import Lootable

@dataclass
class LootData:
    """Loot component for entities.

    This component is used to mark an entity as lootable.
    It can be used to define the loot that an entity drops when it is defeated.
    """
    loot: dict[str, int]

class LootSystem:
    def __init__(self, loot: LootData) -> None:
        """Initialize the LootSystem."""
        self._loot = loot
    
    def drop_loot(self, position: Tuple[int, int], grid_position: Tuple[int,int], size: int) -> None:
        lootable = Lootable(position, grid_position, size, self._loot.loot)
        Event.notify("add_lootable", lootable)
        