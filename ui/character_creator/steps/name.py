import pygame
from settings import get_color
from .creation_step import CreationStep
from .class_ import ClassStep
from ui.utils.text_renderer import draw_text

class NameStep(CreationStep):
    MAX_NAME_LENGTH = 12

    def draw(self) -> None:
        draw_text("Enter characters name", self.center_x, self.center_y-40)
        pygame.draw.rect(self.creator.screen, get_color("light-gray"), (self.center_x-120, self.center_y-20,240,40), 2)
        pygame.draw.rect(self.creator.screen, get_color("black"), (self.center_x-110, self.center_y-15, 220, 30))
        draw_text(f"{self.creator.character_name}", self.center_x, self.center_y)

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.creator.character_name = self.creator.character_name[:-1]
            elif event.key == pygame.K_RETURN:
                if not self.creator.character_name.strip():
                    print("Character name is required.")
                    return
                self.creator.set_step(ClassStep)
            elif len(self.creator.character_name) < self.MAX_NAME_LENGTH and event.unicode.isprintable() and not event.unicode.isspace():
                self.creator.character_name += event.unicode
            