import pygame
from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid import Grid
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
        new_path = self.pathfinder.calculate_path(new_x, new_y)

        if self.movement_manager.can_move(self.entity, len(self.pathfinder.temp_path) + len(new_path) - 1):
            self.grid.navigation_path = self.pathfinder.temp_path + new_path

    def finalize_movement(self, turn_manager: "TurnManager") -> None:
        if self.snap_to_grid():
            self.movement_manager.register_movement(self.entity, len(self.grid.navigation_path) - 1, turn_manager)
        self.pathfinder.clear_path()

    def snap_to_grid(self) -> bool:
        if self.is_out_of_path():
            self.set_position(self.grid.navigation_path[0][0], self.grid.navigation_path[0][1])
            return False
        else:
            last_x, last_y = self.grid.navigation_path[-1]
            self.set_position(last_x, last_y)
            return True

    def is_out_of_path(self) -> bool:
        if not self.grid.navigation_path:
            return False
        
        current_x = floor(self.entity.position.x / self.grid.cell_size)
        current_y = floor(self.entity.position.y / self.grid.cell_size)
        path_start_x, path_start_y = self.grid.navigation_path[0]

        distance = max(abs(current_x - path_start_x), abs(current_y - path_start_y))

        return distance > self.entity.max_tiles
    
    def set_position(self, x: int, y: int) -> None:
        self.entity.set_grid_position(x, y)
        self.entity.position = pygame.Vector2(
            x * self.grid.cell_size + self.grid.cell_size / 4, 
            y * self.grid.cell_size + self.grid.cell_size / 4
        )