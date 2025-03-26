from entities.enemy import Enemy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from movement.movement_manager import MovementManager
    from combat.combat import Combat
    from entities.entity import Entity

class TurnManager:
    def __init__(self, movement_manager: "MovementManager") -> None:
        self.in_combat = False
        self.current_turn_entity = None
        self.movement_manager = movement_manager

    def start_combat(self, combat: "Combat") -> None:
        self.combat = combat
        self.in_combat = True
        combat.display_initiative_order()
        combat.next_turn()

    def end_combat(self) -> None:
        self.in_combat = False
        self.current_turn_entity = None
        self.movement_manager.reset_all_movement()

    def start_turn(self, entity: "Entity") -> None:
        self.current_turn_entity = entity
        self.movement_manager.reset_movement(entity)

        if isinstance(self.current_turn_entity, Enemy):
            entity.ai.update(self.combat.get_player())
            self.end_turn()     

    def next_turn(self) -> None:
        if self.in_combat:
            self.combat.next_turn()

    def end_turn(self) -> None:
        print(f"{self.current_turn_entity.name} finished their turn!")
        self.next_turn()

    def is_current_turn(self, entity: "Entity") -> bool:
        if not self.in_combat:
            return True
        return self.current_turn_entity is entity
    
    def is_in_combat(self) -> bool:
        return self.in_combat