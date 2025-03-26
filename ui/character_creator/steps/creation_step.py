import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character_creator import CharacterCreator
    

class CreationStep(ABC):
    def __init__(self, creator: "CharacterCreator") -> None:
        self.creator = creator

    @property
    def center_x(self) -> int:
        return self.creator.screen.get_width()//2
    
    @property
    def center_y(self) -> int:
        return self.creator.screen.get_height()//2

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event) -> None:
        pass