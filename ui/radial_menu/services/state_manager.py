from typing import Tuple, List, TYPE_CHECKING
from ui.radial_menu.services.event_handler import SectorClickHandler, HoverEffectHandler

if TYPE_CHECKING:
    from ui.radial_menu.components.sector import RadialSector
    import pygame

class RadialMenu:
    def __init__(self, position: Tuple[int, int], sectors: List["RadialSector"]) -> None:
        self.position = position
        self.sectors = sectors
        self._event_handlers = self._init_event_handlers()

    def _init_event_handlers(self):
        return [
            SectorClickHandler(self.sectors),
            HoverEffectHandler(self.sectors)
        ]
    
    def process_events(self):
        pass

    def draw(self, surface: pygame.Surface):
        for sector in self.sectors
            sector.draw(surface)