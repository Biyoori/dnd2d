from typing import TYPE_CHECKING
import pygame

from core.event import Event

if TYPE_CHECKING:
    from entity_manager import GameEntityManager
    from core.grid.grid import Grid
    from ui.feat_menu_manager import FeatMenuManager

class Actions:
    def __init__(self, entity_manager: "GameEntityManager", grid: "Grid", feat_menu_manager: "FeatMenuManager") -> None:
        self.entity_manager = entity_manager
        self.grid = grid
        self.feat_menu_manager = feat_menu_manager

    def attack(self) -> None:
        player = self.entity_manager.get_character()
        enemies = self.entity_manager.get_enemies()
        player.targeting.get_valid_targets(player, enemies, self.grid)

    def abilities(self) -> None:
        player = self.entity_manager.get_character()
        self.feat_menu_manager.create_menu(player)
        selected_feat = self.feat_menu_manager.draw_menu()

        if selected_feat:
            context = {
                "character": player,
                "grid": self.grid,
                "entities": self.entity_manager.get_enemies(),
            }
            
            args = {k: context[k] for k in selected_feat.required_args if k in context}
            
            try:
                selected_feat.execute(**args)
            except ValueError as e:
                print(f"Feat execution failed: {e}")

    def inventory(self) -> None:
        player = self.entity_manager.get_character()

        Event.notify("open_inventory", player)

        


        
