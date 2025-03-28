import math
from typing import Tuple
import pygame

class RadialSector:
    def __init__(self, image: pygame.Surface, hover_image: pygame.Surface, angle_offset: float = 0) -> None:
        self.angle_offset = angle_offset
        self.image = pygame.transform.rotate(image, -self.angle_offset)
        self.hover_image = pygame.transform.rotate(hover_image, -self.angle_offset)
        self.rect = self.image.get_rect()
        self.hovered = False
        self.radius = 120

    def draw(self, surface: pygame.Surface, center_pos: Tuple[int, int]) -> None:
        self.rect.center = center_pos
        current_image = self.hover_image if self.hovered else self.image
        surface.blit(current_image, self.rect)

    def check_hover(self, mouse_pos: Tuple[int, int], menu_center: Tuple[int, int], total_sectors: int) -> bool:
        mouse_x, mouse_y = mouse_pos
        center_x, center_y = menu_center

        distance = math.sqrt((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2)
        if distance > self.radius:
            self.hovered = False
            return False
        
        angle = math.degrees(math.atan2(mouse_y - center_y, mouse_x - center_x))
        angle = (angle + 360 - 60) % 360 

        sector_angle = 360 / total_sectors
        min_angle = self.angle_offset
        max_angle = self.angle_offset + sector_angle

        self.hovered = min_angle <= angle < max_angle
        print(f"Mouse Angle: {angle}, Sector Range: {min_angle}-{max_angle}, Hovered: {self.hovered}")
        return self.hovered