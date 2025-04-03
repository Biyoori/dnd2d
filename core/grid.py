from typing import List, TYPE_CHECKING, Tuple
import pygame
from settings import get_color, screen_width, screen_height

if TYPE_CHECKING:
    from entities.enemy import Enemy

class Grid:
    def __init__(self, size: int = 10, cell_size: int = 64) -> None:
        self._cell_size = cell_size
        self._grid_width = size
        self._grid_height = size
        self._matrix = [[0 for _ in range(self._grid_width)] for _ in range(self._grid_height)]
        self._navigation_path: list[tuple[int, int]] = []
        self._enemy_positions = []

    @property
    def cell_size(self) -> int:
        return self._cell_size
    
    def size(self) -> tuple[int, int]:
        return self._grid_width, self._grid_height
    
    @property
    def navigation_path(self) -> list[tuple[int, int]]:
        return self._navigation_path.copy()
    
    @navigation_path.setter
    def navigation_path(self, new_path: list[tuple[int, int]]) -> None:
        self._navigation_path = new_path
    
    def update_enemy_positions(self, enemies: List["Enemy"]) -> None:
        new_enemy_positions = []
        for enemy in enemies:
            new_enemy_positions.append(tuple(enemy.grid_position))
        self._enemy_positions = new_enemy_positions

    def get_cell_at_position(self, screen_pos: Tuple[int, int]):
        x, y = screen_pos
        if not (0 <= x < screen_width and 0 <= y < screen_height):
            return None
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        return pygame.Vector2(cell_x, cell_y)

    def calculate_path(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> list[tuple[int, int]]:
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        calculated_path = []

        delta_x = abs(end_x - start_x)
        delta_y = abs(end_y - start_y)

        step_x = 1 if start_x < end_x else -1
        step_y = 1 if start_y < end_y else -1
        
        error = delta_x - delta_y

        while end_x != start_x or end_y != start_y:
            calculated_path.append((start_x, start_y))
            doubled_error = 2 * error

            if doubled_error > -delta_y:
                error -= delta_y
                start_x += step_x

            if doubled_error < delta_x:
                error += delta_x
                start_y += step_y

        calculated_path.append((end_x, end_y))   
        return calculated_path
    
    def draw(self, screen: pygame.Surface) -> None:
        gray = get_color("gray")
        green = get_color("green")
        red = get_color("red")
        for row, grid_row in enumerate(self._matrix):
            for col, _ in enumerate(grid_row):
                if (col, row) in self._navigation_path:
                    cell_color = green
                elif (col, row) in self._enemy_positions:
                    cell_color = red
                else:
                    cell_color = gray
                pygame.draw.rect(screen, cell_color, (col*self.cell_size, row*self.cell_size, self.cell_size-1, self.cell_size-1))