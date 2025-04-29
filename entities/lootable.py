from typing import Tuple, Dict
import pygame

from core.event import Event
from settings import get_color
from debugging import logger

class Lootable:
    def __init__(self, position: Tuple[int, int], grid_position: Tuple[int, int], size: int, loot: Dict[str, int]) -> None:
        self._position = position
        self._grid_position = grid_position
        self._size = size
        self._loot = loot
        self._is_looted = False

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        mouse_x, mouse_y = mouse_pos
        click = pygame.Rect.collidepoint(pygame.Rect(self._position[0], self._position[1], self._size, self._size), mouse_pos)
        logger.log(f"Lootable clicked at {mouse_x}, {mouse_y}. position: {self._position} is_clicked: {click}", "DEBUG")


        return click

    def render(self, screen: pygame.Surface, offset: Tuple[int, int]) -> None:
        pygame.draw.rect(
            screen,
            get_color("gold"),  # Złoty kolor dla łupów
            (self._position[0] + offset[0], self._position[1] + offset[1], self._size, self._size),   
        )

    def update_position(self, cell_size: int) -> None:
        self._position = (
            self._grid_position[0] * cell_size + cell_size // 4,
            self._grid_position[1] * cell_size + cell_size // 4
        )
        
    def update_size(self, cell_size: int) -> None:
        self._size = cell_size // 2

    def loot(self) -> Dict[str, int]:
        if not self._is_looted:
            self._is_looted = True
            loot = self._loot.copy()
            Event.notify("remove_lootable", self)
            del self
            return loot
        return {}
    
    def is_looted(self) -> bool:
        return self._is_looted
    