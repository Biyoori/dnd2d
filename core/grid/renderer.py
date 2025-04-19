from typing import TYPE_CHECKING, Tuple
import pygame
from settings import get_color

if TYPE_CHECKING:
    from core.grid.grid import Grid

class GridRenderer:
    def __init__(self, grid: "Grid") -> None:
        self._grid = grid
        self._highlighted_cells = set()

    def render(self, screen: pygame.Surface) -> None:
        floor_color = get_color("gray")
        wall_color = get_color("black")
        green = get_color("green")
        red = get_color("red")
        

        for row, grid_row in enumerate(self._grid.matrix):
            for col, cell in enumerate(grid_row):
                cell_color = wall_color if cell == 1 else floor_color
                pygame.draw.rect(screen, cell_color, (col*self._grid.cell_size, row*self._grid.cell_size, self._grid.cell_size-1, self._grid.cell_size-1))
                if (col, row) in self._highlighted_cells:
                    pygame.draw.rect(
                    screen, 
                    red,
                    (col * self._grid.cell_size, row * self._grid.cell_size, self._grid.cell_size, self._grid.cell_size),
                    3
                )
                    
    def highlight_cells(self, cells: set[Tuple[int, int]]) -> None:
        self._highlighted_cells = cells
