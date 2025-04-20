import pygame

from entities.character.character import Character
from factories.character_factory import CharacterFactory

from .steps import NameStep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .steps.creation_step import CreationStep
    from entities.character.character import Character

class CharacterCreator:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.current_step = NameStep(self)
        self.character_name = ""
        self.character_race = None
        self.character_class = None
        self.skills = []
        self.starting_gear = []

        self._character_created = False

    def run(self) -> None | Character:
        clock = pygame.time.Clock()

        while True:
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                self.current_step.handle_event(event)

                if self._character_created:
                    return self._create_character()
                
            self.current_step.draw()

            pygame.display.flip()
            clock.tick(30)

    def set_step(self, step: "CreationStep") -> None:
        self.current_step = step(self)

    def complete_creation(self) -> None:
        self._character_created = True

    def _create_character(self) -> Character:
        if not all([self.character_name, self.character_class, self.character_race, self.ability_scores, self.skills, self.starting_gear]):
            raise ValueError("Character creation incomplete. Make sure you're not missing anything during creation.")
        return CharacterFactory.create_character(self.character_name, self.character_class, self.character_race, self.ability_scores, self.skills, self.starting_gear)