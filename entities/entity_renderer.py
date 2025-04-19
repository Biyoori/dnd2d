import pygame
from ui.utils.text_renderer import draw_text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid.grid import Grid

class EntityRenderer:
    FEET_PER_STEP = 5
    LABEL_OFFSET_Y = -10

    def __init__(self, entity: "Entity", grid: "Grid") -> None:
        self.entity = entity
        self.grid = grid

    def draw(self, surface: pygame.Surface) -> None:
        combined_path = self.entity.pathfinder.navigation_path + [step for step in self.entity.pathfinder._temp_path if step not in self.entity.pathfinder.navigation_path]
        entity_surface = pygame.Surface((self.entity.size, self.entity.size), pygame.SRCALPHA)
        pygame.draw.rect(entity_surface, self.entity.color, (0, 0, self.entity.size, self.entity.size))
        surface.blit(entity_surface, self.entity.position)

        if combined_path:
            movement_ft = (len(combined_path) - 1) * self.FEET_PER_STEP
            draw_text(f"{movement_ft} ft", self.entity.position.x + self.entity.size // 2, self.entity.position.y - self.LABEL_OFFSET_Y)
