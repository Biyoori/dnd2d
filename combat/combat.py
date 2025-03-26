from typing import List, TYPE_CHECKING
import random
from collections import deque

if TYPE_CHECKING:
    from entities.entity import Entity
    from combat.turn_manager import TurnManager

class Combat:
    def __init__(self, characters: List["Entity"], enemies: List["Entity"], turn_manager: "TurnManager") -> None:
        self.characters = characters
        self.combatants = characters + enemies
        self.turn_queue = deque(self.combatants)
        self.turn_manager = turn_manager

        self.roll_initiative()

    def roll_dice(self, sides) -> int:
        return random.randint(1, sides)

    def roll_initiative(self) -> None:
        self.initiative_order = {}

        for combatant in self.combatants:
            roll = self.roll_dice(20)
            dex_mod = combatant.stats._abilities.get_mod("DEX")
            initiative = roll + dex_mod
            self.initiative_order[combatant] = initiative

        sorted_combatants = sorted(self.initiative_order.keys(), key= lambda c: self.initiative_order[c], reverse=True)

        self.turn_queue = deque(sorted_combatants)

    def display_initiative_order(self) -> None:
        print("\n=== Initiative Order ===")
        for index, (combatant, initiative) in enumerate(
            sorted(self.initiative_order.items(), key=lambda x: x[1], reverse=True)
        ):
            print(f"{index + 1}. {combatant.name} - Initiative: {initiative}")
        print("==============\n")
    
    def next_turn(self) -> None:
        if self.turn_queue:
            current = self.turn_queue.popleft()
            self.turn_queue.append(current)
            self.turn_manager.current_turn_entity = current
            print(f"Now's {current.name}'s turn. Queue: {[entity.name for entity in self.turn_queue]}")
            self.turn_manager.start_turn(current)
        
    def get_player(self) -> "Entity":
        return self.characters[0] if self.characters else None