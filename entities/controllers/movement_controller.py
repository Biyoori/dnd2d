import pygame
from math import floor
from typing import TYPE_CHECKING, List, Tuple
from debugging import logger

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid.grid import Grid
    from movement.movement_manager import MovementManager
    from entities.controllers.entity_pathfinder import EntityPathfinder
    from combat.turn_manager import TurnManager

class EntityMovement:
    def __init__(self, entity: "Entity", grid: "Grid", movement_manager: "MovementManager", pathfinder: "EntityPathfinder") -> None:
        self.entity = entity
        self.grid = grid
        self.movement_manager = movement_manager
        self.pathfinder = pathfinder

    def start_movement(self, path_start_x: int, path_start_y: int) -> None:
        self.pathfinder.start_movement(path_start_x, path_start_y)
        self.movement_used = 0

    def update_movement(self, new_x: int, new_y: int) -> None:
        self.pathfinder.calculate_path(new_x, new_y)
        
    def finalize_movement(self, turn_manager: "TurnManager") -> None:
        combined_path = self.pathfinder.navigation_path + [step for step in self.pathfinder._temp_path if step not in self.pathfinder.navigation_path]
        if not combined_path:
            return
        if self.snap_to_grid(combined_path):
            tiles_moved = len(combined_path) - 1
            self.movement_manager.register_movement(self.entity, tiles_moved, turn_manager)
        self.pathfinder.clear_path()

    def snap_to_grid(self, combined_path: List[Tuple[int,int]]) -> bool:
        if self.is_out_of_path(combined_path):
            self.set_position(combined_path[0][0], combined_path[0][1])
            return False
        else:
            last_x, last_y = combined_path[-1]
            total_path_length = len(combined_path) - 1
            if not self.movement_manager.can_move(self.entity, total_path_length):
                self.set_position(combined_path[0][0], combined_path[0][1])
                return False
            #Check if every step in the path is valid
            for step in combined_path:
                if not self.grid.get_cell(step) == 0:
                    self.set_position(combined_path[0][0], combined_path[0][1])
                    return False
            self.set_position(last_x, last_y)
            return True

    def is_out_of_path(self, combined_path: List[Tuple[int,int]]) -> bool:
        if not self.pathfinder.navigation_path:
            return False
        
        current_x = floor(self.entity.position.x / self.grid.cell_size)
        current_y = floor(self.entity.position.y / self.grid.cell_size)
        path_start_x, path_start_y = combined_path[0]

        distance = max(abs(current_x - path_start_x), abs(current_y - path_start_y))

        return distance > self.entity.max_tiles
    
    def set_position(self, x: int, y: int) -> None:
        self.entity.set_grid_position(x, y)
        self.entity.position = pygame.Vector2(
            x * self.grid.cell_size + self.grid.cell_size / 4, 
            y * self.grid.cell_size + self.grid.cell_size / 4
        )