import pygame
from settings import get_color

_screen = None
_font = None

def init(font_path=None, font_size=32) -> None:
    global _font, _screen
    if font_path:
        _font = pygame.font.Font(font_path, font_size)
    else:
        _font = pygame.font.SysFont(None, font_size)
    _screen = pygame.display.get_surface()

def draw_text(text: str, x: int, y: int, color: tuple[int,int,int]=None, align_center=True, font_size: int=None) -> None:
    if _screen is None or _font is None:
        raise RuntimeError("TextRenderer was not initialized. Try using init() first.")
    
    color = color or get_color("white")
    font = _font if font_size is None else pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)

    if align_center:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))

    _screen.blit(text_surface, text_rect)