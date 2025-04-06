from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from combat.turn_manager import TurnManager

class MovementManager:
    def __init__(self) -> None:
        self.movement_used = {}

    def reset_movement(self, entity: "Entity") -> None:
        self.movement_used[entity] = 0

    def can_move(self, entity: "Entity", tiles: int) -> bool:
        max_tiles = entity.max_tiles
        return self.movement_used.get(entity, 0) + tiles <= max_tiles
    
    def register_movement(self, entity: "Entity", tiles: int, turn_manager: "TurnManager") -> None:
        if turn_manager.is_in_combat():
            if entity in self.movement_used:
                self.movement_used[entity] += tiles
            else:
                self.movement_used[entity] = tiles

            if self.movement_used[entity] >= entity.max_tiles and turn_manager.is_in_combat():
                turn_manager.end_turn()

    def reset_all_movement(self) -> None:
        self.movement_used.clear()