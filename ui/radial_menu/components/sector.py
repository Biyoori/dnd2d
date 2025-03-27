from typing import Tuple
import pygame

class RadialSector:
    def __init__(self, image: pygame.Surface, angle_offset: float = 0) -> None:
        self.angle_offset = angle_offset

        self.image = pygame.transform.rotate(image, -self.angle_offset)
        self.rect = self.image.get_rect()

    def draw(self, surface: pygame.Surface, center_pos: Tuple[int, int]) -> None:
        self.rect.center = center_pos
        surface.blit(self.image, self.rect)