import pygame

from ui.utils.text_renderer import draw_text
from .creation_step import CreationStep
from ..data.classes import get_classes
from .race import RaceStep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character_creator import CharacterCreator

class ClassStep(CreationStep):
    def __init__(self, creator: "CharacterCreator") -> None:
        super().__init__(creator)
        self.classes = get_classes()
        self.selected_index = 0

    def draw(self) -> None:
        current_class = self.classes[self.selected_index]
        draw_text("Pick a class", self.center_x, self.center_y-40)
        draw_text(f"< {current_class.name} >", self.center_x, self.center_y)
        #Implement class description here.

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.classes)
            elif event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.classes)
            elif event.key == pygame.K_RETURN:
                self.creator.character_class = self.classes[self.selected_index]
                self.creator.set_step(RaceStep)