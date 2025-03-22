import pygame
from ui.utils import drawText

class EntityRenderer:

    FEET_PER_STEP = 5
    LABEL_OFFSET_Y = -10

    def __init__(self, entity: "Entity", grid: "Grid"): #type: ignore
        self.entity = entity
        self.grid = grid

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.entity.color, (*self.entity.position, self.entity.size, self.entity.size))

        if self.grid.navigationPath:
            movementFt = (len(self.grid.navigationPath) - 1) * self.FEET_PER_STEP
            drawText(f"{movementFt} ft", self.entity.position.x + self.entity.size // 2, self.entity.position.y - self.LABEL_OFFSET_Y, surface)
