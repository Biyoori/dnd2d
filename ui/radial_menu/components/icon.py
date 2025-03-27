from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple
from settings import get_color_from_pallette
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
    def __init__(self, text: str, font: pygame.font.Font) -> None:
        self.text_surface = font.render(text, True, get_color_from_pallette("white"))