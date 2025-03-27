import math
from typing import Optional, Tuple, List, TYPE_CHECKING
from ui.radial_menu.services.event_handler import SectorClickHandler, HoverEffectHandler
from ui.radial_menu.components.sector import RadialSector
import pygame
if TYPE_CHECKING:
    from ui.radial_menu.components.sector import RadialSector
    from ui.radial_menu.services.event_handler import EventHandler
    

class RadialMenu:
    def __init__(self) -> None:
        self.sectors = [RadialSector(
            image_path="Assets/UI/Rand_Menu/Sectors/rand_menu_sector2.png",
            angle_offset=i * 60
        )
        for i in range(6)
        ]
        self.position = None
        self.active = False
        self.radius = 60

    def _init_event_handlers(self) -> List["EventHandler"]:
        return [
            #SectorClickHandler(self.sectors),
            #HoverEffectHandler(self.sectors)
        ]
    
    def open_at(self, position: Tuple[int, int]) -> None:
        self.position= position
        self.active = True

    def close(self) -> None:
        self.active = False
        self.position = None

    def process_events(self):
        pass

    def draw(self, surface: "pygame.Surface") -> None:
        if not self.active or not self.position:
            return
          
        for i, sector in enumerate(self.sectors):
            
            angle = (i*60 + 90)

            x = self.position[0] + self.radius * math.cos(math.radians(angle))
            y = self.position[1] + self.radius * math.sin(math.radians(angle))
            
            sector.draw(surface, (x,y))