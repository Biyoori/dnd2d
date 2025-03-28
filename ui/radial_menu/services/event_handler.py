from abc import ABC, abstractmethod
from typing import List, Tuple
from ui.radial_menu.components.sector import RadialSector
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
    def __init__(self, sectors: List[RadialSector], menu_center: Tuple[int, int], sector_count: int) -> None:
        self.sectors = sectors
        self.menu_center = menu_center
        self.sector_count = sector_count

    def handle(self, event: "pygame.event.Event") -> bool:
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for sector in self.sectors:
                sector.check_hover(mouse_pos, self.menu_center, self.sector_count)
        return False
