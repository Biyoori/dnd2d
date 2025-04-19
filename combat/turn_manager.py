from core.event import Event
from entities.enemy import Enemy
from typing import TYPE_CHECKING
from ui.game_console import console
from entities.entity import Entity

if TYPE_CHECKING:
    from movement.movement_manager import MovementManager
    from combat.combat import Combat
    from entities.entity import Entity

class TurnManager:
    def __init__(self, movement_manager: "MovementManager") -> None:
        self.in_combat = False
        self.current_turn_entity = None
        self.movement_manager = movement_manager
        self.actions_remaining = 0
        self.bonus_action_used = False

        Event.subscribe("use_action", self.use_action)
        Event.subscribe("use_bonus_action", self.use_bonus_action)

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

        self.actions_remaining = 1
        self.bonus_action_used = False

        if isinstance(self.current_turn_entity, Enemy):
            entity.ai.update(self.combat.get_player())
            self.end_turn()     

    def next_turn(self) -> None:
        if self.in_combat:
            self.combat.next_turn()

    def end_turn(self) -> None:
        console.log(f"{self.current_turn_entity.name} finished their turn!")
        self.next_turn()

    def is_current_turn(self, entity: "Entity") -> bool:
        if not self.in_combat:
            return True
        return self.current_turn_entity is entity
    
    def is_in_combat(self) -> bool:
        return self.in_combat
    
    def use_action(self) -> bool:
        if self.actions_remaining > 0:
            self.actions_remaining -= 1
            console.log(f"{self.current_turn_entity.name} used an action. Actions left: {self.actions_remaining}")
            return True
        console.log("No actions remaining!")
        return False
    
    def use_bonus_action(self) -> bool:
        if not self.bonus_action_used:
            self.bonus_action_used = True
            console.log(f"{self.current_turn_entity.name} used a bonus action.")
            return True
        console.log("Bonus action already used!")
        return False
    
    def has_action(self) -> bool:
        return self.actions_remaining > 0
    
    def has_bonus_action(self) -> bool:
        return not self.bonus_action_used
        
    def get_current_entity(self):
        return self.current_turn_entity