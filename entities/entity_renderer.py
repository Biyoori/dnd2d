import pygame
from ui.utils.text_renderer import draw_text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid import Grid

class EntityRenderer:
    FEET_PER_STEP = 5
    LABEL_OFFSET_Y = -10

    def __init__(self, entity: "Entity", grid: "Grid") -> None:
        self.entity = entity
        self.grid = grid

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.entity.color, (*self.entity.position, self.entity.size, self.entity.size))

        if self.grid.navigation_path:
            movement_ft = (len(self.grid.navigation_path) - 1) * self.FEET_PER_STEP
            draw_text(f"{movement_ft} ft", self.entity.position.x + self.entity.size // 2, self.entity.position.y - self.LABEL_OFFSET_Y)
