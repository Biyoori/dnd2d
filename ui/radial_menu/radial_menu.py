from entity_manager import GameEntityManager
from ui.radial_menu.components.sector_actions import Actions
from ui.radial_menu.services.renderer import MenuRenderer
from .services.positioning import MenuPositioning
from .services.event_handler import SectorClickHandler, HoverEffectHandler, EventHandler
from ui.radial_menu.components.sector_factory import SectorFactory
from .components.sector import RadialSector
from typing import Tuple, List, TYPE_CHECKING 
import pygame

if TYPE_CHECKING:
    from core.grid import Grid
    from ui.feat_menu_manager import FeatMenuManager


class RadialMenu:
    def __init__(self, entity_manager: GameEntityManager, grid: "Grid", feat_menu_manager: "FeatMenuManager") -> None:
        self.active: bool = False
        self.radius: int = 60  

        self.positioning = MenuPositioning()
        self.renderer = MenuRenderer()
        self.factory = SectorFactory(self.renderer.font)
        
        self.actions = Actions(entity_manager, grid, feat_menu_manager)
            
        images = self.renderer.load_images()
        self.sectors = self._create_sectors(*images)
        self._event_handlers = self._init_event_handlers()

    def _create_sectors(self, base_img:pygame.surface, hover_img: pygame.Surface) -> List[RadialSector]:
        sector_data = [
            ("Attack", self.actions.attack),
            ("Magic", self.actions.attack),
            ("Flee", self.actions.attack),
            ("Abilities", self.actions.abilities),
            ("Items", self.actions.attack),
            ("Help", self.actions.attack)
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

    def enable_sector(self, sector_name: str, enable: bool = True) -> None:
        for sector in self.sectors:
            if sector.icon and sector.icon.text == sector_name:
                sector.enabled = enable
                break
        
    def enable_all_sectors(self, enable: bool = True) -> None:
        for sector in self.sectors:
            sector.enabled = enable

    def get_sector(self, sector_name: str):
        for sector in self.sectors:
            if sector.icon and sector.icon.text == sector_name:
                return sector
            return None