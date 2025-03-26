import pygame
from .creation_step import CreationStep
from ..data.races import get_races
from .abilities import AbilityStep
from ui.utils.text_renderer import draw_text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character_creator import CharacterCreator

class RaceStep(CreationStep):
    def __init__(self, creator: "CharacterCreator") -> None:
        super().__init__(creator)
        self.races = get_races()
        self.selected_index = 0

    def draw(self) -> None:
        draw_text("Pick a race", self.center_x, self.center_y-40)
        current_race = self.races[self.selected_index]
        draw_text(f"< {current_race.name} >", self.center_x, self.center_y)
        #Race bonuses drawing implementation here.

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.races)
            elif event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.races)
            elif event.key == pygame.K_RETURN:
                self.creator.character_race = self.races[self.selected_index]
                self.creator.set_step(AbilityStep)