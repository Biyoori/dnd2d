from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from combat.turn_manager import TurnManager

class TurnInfo:
    def __init__(self, turn_manager: "TurnManager", screen: pygame.Surface) -> None:
        self.turn_manager = turn_manager
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        entity_name = f"{self.turn_manager.get_current_entity().name}" if self.turn_manager.get_current_entity() else "None"
        text = f"{entity_name} | Actions: {self.turn_manager.actions_remaining} | Bonus: {'Yes' if self.turn_manager.has_bonus_action() else 'No'}"
        ui_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(ui_surface, (20, 20))