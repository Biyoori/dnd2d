from abc import ABC, abstractmethod
from typing import Tuple
from settings import get_color
from ui.utils.graphics_loader import load_image
import pygame
    

class Icon(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

class ImageIcon(Icon):
    def __init__(self, image_path: str) -> None:
        self.image = load_image(image_path) or pygame.Surface((64, 64))
        if self.image is None:
            raise ValueError(f"Cant load the icon from {image_path}")

    def draw(self, surface: pygame.Surface, pos: Tuple[int, int]) -> None:
        surface.blit(self.image, pos)

class TextIcon(Icon):
    def __init__(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int] = get_color("white")) -> None:
        self.text = text
        self.font = font
        self.color = color
        self.text_surface = font.render(text, True, color)
        self.rect = self.text_surface.get_rect()

    def draw(self, surface: pygame.Surface, pos: Tuple[int, int]) -> None:
        self.rect.center = pos
        surface.blit(self.text_surface, self.rect)