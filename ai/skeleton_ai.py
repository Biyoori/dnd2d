from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid import Grid


class SkeletonAi:
    def __init__(self, entity: "Entity", grid: "Grid") -> None:
        self.entity = entity
        self.grid = grid

    def update(self, target: "Entity") -> None:
        melee_action = next((action for action in self.entity.actions if action["name"] == "Shortsword"), None)

        if melee_action and self.is_in_melee_range(target, melee_action["range"]/5):
            self.entity.execute_action("Shortsword", target)        
        else:
            path = self.grid.calculate_path(self.entity.grid_position, target.grid_position)
            next_step = path[1]
            self.entity.set_grid_position(*next_step)
            self.entity.set_position(self.grid)

    def is_in_melee_range(self, target: "Entity", attack_range: int) -> bool:
        dx: int = abs(self.entity.grid_position[0] - target.grid_position[0])
        dy: int = abs(self.entity.grid_position[1] - target.grid_position[1])

        return dx <= attack_range//5 and dy <= attack_range