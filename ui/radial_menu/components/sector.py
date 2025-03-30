from typing import Tuple, Optional
from ..components.icon import Icon, TextIcon
import math
import pygame

class RadialSector:
    def __init__(self, image: pygame.Surface, hover_image: pygame.Surface, angle_offset: float = 0, icon: Optional[Icon] = None, icon_offset: float = 0.6, task: callable = None) -> None:
        self.angle_offset = angle_offset
        self.image = pygame.transform.rotate(image, -self.angle_offset)
        self.hover_image = pygame.transform.rotate(hover_image, -self.angle_offset)
        self.rect = self.image.get_rect()
        self.hovered = False
        self.radius = 120
        self.enabled = True

        #Icon
        self.icon = icon
        self.icon_offset = icon_offset

        self.task = task

    def draw(self, surface: pygame.Surface, center_pos: Tuple[int, int]) -> None:
        self.rect.center = center_pos
        current_image = self.hover_image if self.hovered else self.image   

        if not self.enabled:
            current_image = current_image.copy()
            current_image.fill((100, 100, 100, 150), special_flags=pygame.BLEND_MULT)

        surface.blit(current_image, self.rect)

        if self.icon:
            angle_rad = math.radians(self.angle_offset + 90)
            icon_distance = self.radius / 4
            icon_x = center_pos[0] + icon_distance * math.cos(angle_rad)
            icon_y = center_pos[1] + icon_distance * math.sin(angle_rad)

        if not self.enabled and isinstance(self.icon, TextIcon):
            self.icon.color = (100, 100, 100)
            self.icon.text_surface = self.icon.font.render(self.icon.text, True, self.icon.color)

        self.icon.draw(surface, (icon_x, icon_y))

    def check_hover(self, mouse_pos: Tuple[int, int], menu_center: Tuple[int, int], total_sectors: int) -> bool:
        if not self.enabled:
            self.hovered = False
            return False
        
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
        return self.hovered
    
    def on_click(self) -> None:
        self.task()