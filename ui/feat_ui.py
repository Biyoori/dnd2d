from typing import TYPE_CHECKING, List, Optional
import pygame

from settings import get_color

if TYPE_CHECKING:
    from entities.entity import Entity
    from feat import Feat

class FeatMenu:
    def __init__(self, character: "Entity", screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.character = character
        self.screen = screen
        self.font = font
        self.available_feats = self._get_available_feats()
        self.buttons: List[pygame.Rect] = []
        self.cancel_button = pygame.Rect(0, 0, 0, 0)
        self.menu_rect = pygame.Rect(10, 10, 350, 400)
        self.alpha = 180

        self.menu_surface = pygame.Surface((self.menu_rect.width, self.menu_rect.height), pygame.SRCALPHA)

    def _get_available_feats(self) -> dict[str, "Feat"]:
        return {
            name: feat
            for name, feat in self.character.feats.get_feats().items()
            if not feat.is_passive and name in self.character.feats.get_active()
        }
    
    def draw(self) -> None:       
        self.menu_surface.fill((0, 0, 0, 0))

        pygame.draw.rect(self.menu_surface, get_color("dark-gray"), (0, 0, self.menu_rect.width, self.menu_rect.height))
        pygame.draw.rect(self.menu_surface, get_color("gold"), (0, 0, self.menu_rect.width, self.menu_rect.height), 1)

        self.buttons.clear()

        title = self.font.render("Select Feat:", True, get_color("white"))
        self.menu_surface.blit(title, (20, 20))

        for i, (name, feat) in enumerate(self.available_feats.items()):
            y_pos = 60 + i * 40
            button_rect = pygame.Rect(20, y_pos, self.menu_rect.width - 40, 35)
            self.buttons.append(pygame.Rect(self.menu_rect.x + button_rect.x, self.menu_rect.y + button_rect.y, button_rect.width, button_rect.height))

            pygame.draw.rect(self.menu_surface, get_color("gold"), button_rect, 1)
            pygame.draw.rect(self.menu_surface, (50, 50, 50, self.alpha), button_rect.inflate(-4, -4))

            feat_text = self.font.render(f"{name}", True, get_color("white"))
            self.menu_surface.blit(feat_text, (button_rect.x + 10, button_rect.y + 8))

        cancel_rect = pygame.Rect(self.menu_rect.width//2 - 50, self.menu_rect.height - 50, 100, 30)
        pygame.draw.rect(self.menu_surface, get_color("gold"), cancel_rect, 1)
        pygame.draw.rect(self.menu_surface, (80, 30, 30, self.alpha), cancel_rect.inflate(-4, -4))

        cancel_text = self.font.render("Cancel", True, get_color("white"))
        self.menu_surface.blit(cancel_text, (self.cancel_button.x + 15, self.cancel_button.y-5))

        self.cancel_button = pygame.Rect(
            self.menu_rect.x + cancel_rect.x,
            self.menu_rect.y + cancel_rect.y,
            cancel_rect.width, cancel_rect.height
        )
        
        self.screen.blit(self.menu_surface, (self.menu_rect.x, self.menu_rect.y))
        pygame.display.update(self.menu_rect)

    def handle_events(self) -> Optional["Feat"]:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.cancel_button.collidepoint(mouse_pos):
                        return None
            
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(mouse_pos):
                            selected = list(self.available_feats.values())[i]
                            return selected
                    
            self.draw()
            pygame.time.delay(30)        