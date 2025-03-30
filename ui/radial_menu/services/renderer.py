from ui.utils.graphics_loader import load_image
from typing import TYPE_CHECKING, Tuple
import pygame

if TYPE_CHECKING:
    from ui.radial_menu.components.sector import RadialSector

class MenuRenderer:
    def __init__(self) -> None:
        self.font = pygame.font.Font("Assets/UI/Fonts/IM_Fell_DW_Pica/IMFellDWPica-Regular.ttf", 24)
        self.base_img, self.hover_img = self.load_images()

    def render(self, surface: pygame.Surface, sector: "RadialSector", position: Tuple[int,int]) -> None:
        sector.draw(surface, position)

    def load_images(self) -> Tuple[pygame.Surface]:
        base_image = load_image("Assets/UI/Radial_Menu/Sector.png")
        hover_image = load_image("Assets/UI/Radial_Menu/Hover.png")
        border = load_image("Assets/UI/Radial_Menu/Border.png")

        combined = pygame.Surface((120, 120), pygame.SRCALPHA)
        combined.blit(base_image, (0, 0))
        combined.blit(border, (0, 0))

        combined_hover = pygame.Surface((120, 120), pygame.SRCALPHA)
        combined_hover.blit(hover_image, (0, 0))
        combined_hover.blit(border, (0, 0))

        return combined, combined_hover