from typing import TYPE_CHECKING, Tuple, List
if TYPE_CHECKING:
    from core.grid.grid import Grid
    from entities.entity import Entity

class GridObjectsManager:
    def __init__(self, grid: "Grid") -> None:
        self.grid = grid
        self.enemies = []
        self.objects = []
    
    def add_enemy(self, enemy: "Entity", position: Tuple[int, int]) -> None:
        self.enemies.append((enemy, position))

    def add_object(self, obj: "Entity", position: Tuple[int, int]) -> None:
        self.objects.append((obj, position))

    def remove_object(self, obj: "Entity") -> None:
        self.objects = [(o, p) for o, p in self.objects if o != obj]
    
    def get_objects_at(self, position: Tuple[int, int]) -> List["Entity"]:
        return [o for o, p in self.objects if p == position]
    
    def get_enemy_positions(self) -> List[Tuple[int, int]]:
        return [p for _, p in self.enemies]

    