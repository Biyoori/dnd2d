from typing import TYPE_CHECKING, List, Tuple
import pygame

if TYPE_CHECKING:
    from entities.components.factions import FactionSystem
    from entities.entity import Entity
    from core.grid import Grid
    from entities.components.attack import AttackSystem
    from combat.turn_manager import TurnManager

class TargetingSystem:
    def __init__(self, faction_system: "FactionSystem") -> None:
        self.faction_system = faction_system
        self.current_valid_targets: List["Entity"] = []
        self.target_selection = False


    def get_valid_targets(self, attacker: "Entity", entities: List["Entity"], grid: "Grid") -> List["Entity"]:
        self.current_valid_targets = []
        print(self.current_valid_targets)

        for enemy in self.faction_system.get_enemies(entities, attacker.faction):
            if self._is_in_range(attacker, enemy, attacker.weapon_system.get_equipped_weapon().range//5):
                self.current_valid_targets.append(enemy)
                print(enemy.grid_position)

        grid.update_enemy_positions(self.current_valid_targets)
        self.target_selection = True
        return self.current_valid_targets
    
    def _is_in_range(self, attacker: "Entity", target: "Entity", range: int) -> bool:
        attacker_position_x, attacker_position_y = attacker.grid_position
        attacker_position = pygame.Vector2(attacker_position_x, attacker_position_y)
        distance = max(abs(attacker_position_x - target.grid_position[0]), abs(attacker_position_y - target.grid_position[1]))
        return distance <= range
    
    def handle_target_selection(self, mouse_pos: Tuple[int, int], grid: "Grid", attack_system: "AttackSystem", attacker: "Entity", turn_manager: "TurnManager") -> bool:
        clicked_cell = grid.get_cell_at_position(mouse_pos)
        if clicked_cell is None:
            return False
        
        for target in self.current_valid_targets:
            if (target.grid_position[0], target.grid_position[1]) == (clicked_cell[0], clicked_cell[1]):
                if turn_manager.use_action():
                    attack_system.resolve_attack(attacker, target)
                grid.update_enemy_positions([])
                self.target_selection = False
                return True
        return False