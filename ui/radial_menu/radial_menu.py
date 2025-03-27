import math
import pygame
from typing import Tuple, List

from ui.utils.graphics_loader import load_image
from .components.sector import RadialSector
from .services.event_handler import SectorClickHandler, HoverEffectHandler, EventHandler

class RadialMenu:
    def __init__(self, sector_count: int = 6) -> None:
        base_image = load_image("Assets/UI/Radial_Menu/Sector.png")
        border = load_image("Assets/UI/Radial_Menu/Border.png")
        combined = pygame.Surface((120,120), pygame.SRCALPHA)
        combined.blit(base_image,(0,0))
        combined.blit(border,(0,0))
        self.sectors = [
            RadialSector(combined, i * (360/sector_count))
            for i in range(sector_count)
        ]

        self.position: Tuple[int, int] = None
        self.active: bool = False
        self.radius: int = 60

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

    def process_events(self):
        pass

    def draw(self, surface: "pygame.Surface") -> None:
        if not self.active:
            return
          
        for i, sector in enumerate(self.sectors):        
            angle = math.radians(i * (360 / len(self.sectors)) + 90)

            x = self.position[0] + self.radius * math.cos(angle)
            y = self.position[1] + self.radius * math.sin(angle)
            
            sector.draw(surface, (x,y))