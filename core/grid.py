import pygame
from settings import get_color

class Grid:
    def __init__(self, size: int = 10, cell_size: int = 64) -> None:
        self._cell_size = cell_size
        self._size = size
        self._matrix = [[0 for _ in range(size)] for _ in range(size)]
        self._navigation_path: list[tuple[int, int]] = []

    @property
    def cell_size(self) -> int:
        return self._cell_size
    
    def size(self) -> int:
        return self._size
    
    @property
    def navigation_path(self) -> list[tuple[int, int]]:
        return self._navigation_path.copy()
    
    @navigation_path.setter
    def navigation_path(self, new_path: list[tuple[int, int]]) -> None:
        self._navigation_path = new_path

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

        for row, grid_row in enumerate(self._matrix):
            for col, _ in enumerate(grid_row):
                cell_color = green if (col, row) in self._navigation_path else gray    
                pygame.draw.rect(screen, cell_color, (col*self.cell_size, row*self.cell_size, self.cell_size-1, self.cell_size-1))