from core.grid.dungeon_generator import DungeonGenerator
from core.grid.objects_manager import GridObjectsManager
from core.grid.renderer import GridRenderer
from .pathfinding import Pathfinding
from typing import Tuple, List, TYPE_CHECKING

class Grid:
    def __init__(self, size: int = 20, cell_size: int = 64) -> None:
        self.cell_size = cell_size
        self._grid_width = size
        self._grid_height = size
        self._matrix = [[0 for _ in range(self._grid_width)] for _ in range(self._grid_height)]

        self.pathfinding = Pathfinding(self)
        self.object_manager = GridObjectsManager(self)
        self.renderer = GridRenderer(self)
        self.generator = DungeonGenerator(self)

    
    def size(self) -> tuple[int, int]:
        return self._grid_width, self._grid_height
    
    @property
    def matrix(self) -> list[list[int]]:
        return self._matrix.copy()
    
    def set_cell(self, x: int, y: int, value: int) -> None:
        if 0 <= x < self._grid_width and 0 <= y < self._grid_height:
            self._matrix[y][x] = value

    def get_cell_from_pos(self, screen_pos: Tuple[int, int]):
        x, y = screen_pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        return grid_x, grid_y
    
    def get_cell(self, pos: Tuple[int, int]) -> int:
        x, y = pos
        if 0 <= x < self._grid_width and 0 <= y < self._grid_height:
            return self._matrix[y][x]
        return -1
    
    def clear_matrix(self) -> None:
        self._matrix = [[1 for _ in range(self._grid_width)] for _ in range(self._grid_height)]
    
    