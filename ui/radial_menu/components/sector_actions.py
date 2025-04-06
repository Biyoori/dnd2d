from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity_manager import GameEntityManager
    from core.grid import Grid

class Actions:
    def __init__(self, entity_manager: "GameEntityManager", grid: "Grid") -> None:
        self.entity_manager = entity_manager
        self.grid = grid

    def attack(self) -> None:
        player = self.entity_manager.get_character()
        enemies = self.entity_manager.get_enemies()
        player.targeting.get_valid_targets(player, enemies, self.grid)

    def abilities(self):
        player = self.entity_manager.get_character()
        player.feats.execute("Talons", grid=self.grid, entities=self.entity_manager.get_enemies())