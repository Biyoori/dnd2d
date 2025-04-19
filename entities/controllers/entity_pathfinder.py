from hmac import new
from webbrowser import get
from movement import movement_manager
from settings import get_color
from typing import TYPE_CHECKING, List, Tuple
import pygame

if TYPE_CHECKING:
    from core.grid.grid import Grid
    from entities.entity import Entity
    from movement.movement_manager import MovementManager

class EntityPathfinder:
    def __init__(self, entity: "Entity", grid: "Grid", movement_manager: "MovementManager") -> None:
        self.entity = entity
        self._grid = grid
        self._movement_manager = movement_manager
        self._temp_path = []
        self._navigation_path = []
        self._path_start_x, self._path_start_y = 0, 0

    @property
    def navigation_path(self) -> Tuple[int, int]:
        return self._navigation_path.copy()
    
    def extend_path(self, new_path: List[Tuple[int, int]]) -> None:
        self._navigation_path.append(new_path)


    def start_movement(self, path_start_x: int, path_start_y: int) -> None:
        self._path_start_x, self._path_start_y = path_start_x, path_start_y
        self._navigation_path = [(path_start_x, path_start_y)]

    def break_path(self) -> None:
        for step in self._temp_path:
            if step not in self._navigation_path:
                self._navigation_path.append(step)
        self._temp_path = []
        self._path_start_x, self._path_start_y = self._navigation_path[-1]

    def calculate_path(self, new_x: int, new_y: int) -> list[tuple[int, int]]:
        self._temp_path = self._grid.pathfinding.find_path((self._path_start_x, self._path_start_y), (new_x, new_y))
        return self._temp_path
           
    def clear_path(self) -> None:
        self._navigation_path = []
        self._temp_path = []

    def draw_path(self, screen: pygame.Surface, cell_size: int) -> None:
        yellow = get_color("yellow")
        red = get_color("red")
        green = get_color("green")
        
        combined_path = list(dict.fromkeys(self._navigation_path + self._temp_path))

        pixel_positions = [
            (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
            for x, y in combined_path
        ]

        for i in range(len(combined_path) - 1):
            pygame.draw.line(screen, yellow, pixel_positions[i], pixel_positions[i + 1], 2)

        can_move_results = [
            self._movement_manager.can_move(self.entity, index) 
            for index in range(len(combined_path))
        ]

        for (x, y), can_move in zip(combined_path, can_move_results):
            color = green if can_move else red
            pygame.draw.rect(
                screen, 
                color, 
                (x * cell_size, y * cell_size, cell_size -1, cell_size -1), 
                1
            )