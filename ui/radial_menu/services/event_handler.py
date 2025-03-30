from abc import ABC, abstractmethod
from math import e
from typing import List, Tuple
from ui.radial_menu.components.sector import RadialSector
import pygame

class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: "pygame.event") -> bool:
        pass

class SectorClickHandler(EventHandler):
    def __init__(self, sectors: List[RadialSector]) -> None:
        self.sectors = sectors
        self.sector_count = 6

    def update_menu_center(self, new_center: Tuple[int,int]) -> None:
        self._menu_center = new_center

    def handle(self, event: pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for sector in self.sectors:
                if sector.enabled and sector.check_hover(mouse_pos, self._menu_center, self.sector_count):
                    sector.on_click()
        
class HoverEffectHandler(EventHandler):
    def __init__(self, sectors: List[RadialSector]) -> None:
        self.sectors = sectors
        self.sector_count = 6

    def update_menu_center(self, new_center: Tuple[int,int]) -> None:
        self._menu_center = new_center

    def handle(self, event: pygame.event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for sector in self.sectors:
                sector.check_hover(mouse_pos, self._menu_center, self.sector_count)
        return False
