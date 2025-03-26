from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.grid import Grid

class EntityPathfinder:
    def __init__(self, grid: "Grid") -> None:
        self.grid = grid
        self._temp_path = []
        self.path_start_x, self.path_start_y = 0, 0

    @property
    def temp_path(self) -> list[tuple[int, int]]:
        return self._temp_path.copy()

    def start_movement(self, path_start_x: int, path_start_y: int) -> None:
        self.path_start_x, self.path_start_y = path_start_x, path_start_y
        self.grid.navigation_path = [(path_start_x, path_start_y)]
        self._temp_path = []

    def update_path(self) -> None:
        if len(self.grid.navigation_path) > 1:
            self._temp_path = self.grid.navigation_path[:-1]
            self.path_start_x, self.path_start_y = self.grid.navigation_path[-1]

    def calculate_path(self, new_x: int, new_y: int) -> list[tuple[int, int]]:
        return self.grid.calculate_path((self.path_start_x, self.path_start_y), (new_x, new_y))
    
    def clear_path(self) -> None:
        self._temp_path = []
        self.grid.navigation_path = []