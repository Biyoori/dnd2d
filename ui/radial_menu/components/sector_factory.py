import pygame
from settings import get_color
from typing import Callable
from ...radial_menu.components.icon import ImageIcon, TextIcon
from ...radial_menu.components.sector import RadialSector


class SectorFactory:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font
        self.color = get_color("gold")

    def create_sector(self, name: str, base_img: pygame.Surface, hover_img: pygame.Surface, angle: int, task: Callable = None) -> RadialSector:
        icon = TextIcon(name, self.font, self.color)
        return RadialSector(base_img, hover_img, angle, icon, task=task)
    
