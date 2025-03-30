from ui.radial_menu.services.renderer import MenuRenderer
from .services.positioning import MenuPositioning
from .services.event_handler import SectorClickHandler, HoverEffectHandler, EventHandler
from ui.radial_menu.components.sector_factory import SectorFactory
from .components.sector import RadialSector
from typing import Callable, Tuple, List, Dict
import pygame


class RadialMenu:
    def __init__(self, action_handlers: Dict[str, Callable]) -> None:
        self.active: bool = False
        self.radius: int = 60  

        self.positioning = MenuPositioning()
        self.renderer = MenuRenderer()
        self.factory = SectorFactory(self.renderer.font)
        
        self.actions = action_handlers
            
        images = self.renderer.load_images()
        self.sectors = self._create_sectors(*images)
        self._event_handlers = self._init_event_handlers()

    def _create_sectors(self, base_img:pygame.surface, hover_img: pygame.Surface) -> List[RadialSector]:
        sector_data = [
            ("Attack", self._execute_attack),
            ("Magic", self._execute_attack),
            ("Flee", self._execute_attack),
            ("Abilities", self._execute_attack),
            ("Items", self._execute_attack),
            ("Help", self._execute_attack)
        ]

        return [
            self.factory.create_sector(name, base_img, hover_img, i * self.radius, task)
            for i, (name, task) in enumerate(sector_data)
        ]
        
    def _init_event_handlers(self) -> List["EventHandler"]:
        return [
            SectorClickHandler(self.sectors),
            HoverEffectHandler(self.sectors)
        ]
    
    def _update_handlers_position(self):
        for handler in self._event_handlers:
            if hasattr(handler, "update_menu_center"):
                handler.update_menu_center(self.positioning.position)

    def open_at(self, position: Tuple[int, int]) -> None:
        self.positioning.position = position
        self._update_handlers_position()
        self.active = True

    def close(self) -> None:
        self.active = False

    def process_events(self, event: pygame.event.Event) -> None:
        if not self.active:
            return

        for handler in self._event_handlers:
            handler.handle(event)

    def draw(self, surface: "pygame.Surface") -> None:
        if not self.active:
            return        

        for i, sector in enumerate(self.sectors):
            pos = self.positioning.calculate_position(i)
            self.renderer.render(surface, sector, pos)
    
    def _execute_attack(self) -> None:
        if "attack" in self.actions:
            self.actions["attack"]()