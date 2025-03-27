from turtle import pos
from typing import TYPE_CHECKING, Tuple

from ui.utils.graphics_loader import load_image
import pygame

if TYPE_CHECKING:
    from ui.radial_menu.components.icon import Icon

class RadialSector:
    def __init__(self, image_path: str, angle_offset: float = 0) -> None:
        print(load_image(image_path))
        self.base_image = load_image(image_path)
        self.angle_offset = angle_offset

        original_center = self.base_image.get_rect().center
        self.current_image = pygame.transform.rotate(self.base_image, -angle_offset)
        self.rect = self.current_image.get_rect()

    def draw(self, surface: pygame.Surface, center_pos: Tuple[int, int]) -> None:
        self.rect.center = center_pos
        surface.blit(self.current_image, self.rect)