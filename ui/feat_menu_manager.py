from ui.feat_ui import FeatMenu
from typing import Optional, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from entities.entity import Entity
    from feat import Feat

class FeatMenuManager:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font("Assets/UI/Fonts/IM_Fell_DW_Pica/IMFellDWPica-Regular.ttf", 18)
        self.current_menu: Optional[FeatMenu] = None

    def create_menu(self, character: "Entity") -> None:
        self.current_menu = FeatMenu(character, self.screen, self.font)

    def draw_menu(self):
        if not self.current_menu:
            return None
        return self.current_menu.handle_events()