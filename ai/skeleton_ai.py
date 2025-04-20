from debugging import logger
from operator import is_
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid.grid import Grid


class SkeletonAi:
    def __init__(self, entity: "Entity", grid: "Grid") -> None:
        self.entity = entity
        self.grid = grid

    def update(self, target: "Entity") -> None:
        melee_action = next((action for action in self.entity.actions if action["name"] == "Shortsword"), None)
        range_action = next((action for action in self.entity.actions if action["name"] == "Shortbow"), None)

        range = range_action["range"] if range_action else 0
        range = range.split("/") if "/" in range else int(range)
        range = int(range[0]) if isinstance(range, list) else int(range)


        if melee_action and self.is_in_melee_range(target, melee_action["range"]//5):
            self.entity.execute_action("Shortsword", target)
            self.log_decision(f"Attacking target at {target.grid_position} with melee action.")
        elif range_action and self.is_in_range(target, range//5):
            self.entity.execute_action("Shortbow", target)      
            self.log_decision(f"Attacking target at {target.grid_position} with ranged action.")  
        else:
            self._move_to_target(target)
            if melee_action and self.is_in_melee_range(target, melee_action["range"]//5):
                self.entity.execute_action("Shortsword", target)
                self.log_decision(f"Attacking target at {target.grid_position} with melee action after moving.")
            elif range_action and self.is_in_range(target, range//5):
                self.log_decision(f"Attacking target at {target.grid_position} with ranged action after moving.")
                self.entity.execute_action("Shortbow", target)

    def is_in_melee_range(self, target: "Entity", attack_range: int) -> bool:
        dx: int = abs(self.entity.grid_position[0] - target.grid_position[0])
        dy: int = abs(self.entity.grid_position[1] - target.grid_position[1])

        return dx <= attack_range and dy <= attack_range and (dx + dy == 1 or (dx == 1 and dy == 1))
    
    def is_in_range(self, target: "Entity", attack_range: int) -> bool:
        dx: int = abs(self.entity.grid_position[0] - target.grid_position[0])
        dy: int = abs(self.entity.grid_position[1] - target.grid_position[1])

        return dx <= attack_range and dy <= attack_range or (dx + dy <= attack_range and dx != 0 and dy != 0)

    def _move_to_target(self, target: "Entity") -> None:
        self.log_decision(f"Moving towards target at {target.grid_position}")
        path = self.grid.pathfinding.find_path_a_star(tuple(self.entity.grid_position), tuple(target.grid_position))

        if not path:
            self.log_decision("No path found to target.")
            return

        speed = self.entity.speed // 5
        steps_to_take = min(speed, len(path) - 1)
        for step in range(1, steps_to_take + 1):
            next_step = path[step]
            if next_step == tuple(target.grid_position):
                break

            self.entity.set_grid_position(*next_step)
            self.entity.set_position(self.grid)

    def log_decision(self, message: str) -> None:
        logger.log(f"SkeletonAI: {message}", "AI")

    def draw_path(self, path: list, screen: pygame.Surface) -> None:
        for step in path:
            x, y = step
            pygame.draw.rect(screen, (255, 0, 0), (x * self.grid.cell_size, y * self.grid.cell_size, self.grid.cell_size, self.grid.cell_size), 1)