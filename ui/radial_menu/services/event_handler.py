from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame

class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: "pygame.event.Event") -> bool:
        pass

class SectorClickHandler(EventHandler):
    def handle(self, event: "pygame.event.Event") -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._check_sector_collision(event.pos)
        
class HoverEffectHandler(EventHandler):
    def handle(self, event: "pygame.event.Event") -> bool:
        pass