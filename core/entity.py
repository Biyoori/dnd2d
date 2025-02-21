import pygame
from typing import Optional

class Entity:
    def __init__(self, x: Optional[int], y: Optional[int], cellSize: Optional[int], color: tuple[int,int,int]):
        if x and y and cellSize:
            self.position = pygame.Vector2(
                x * cellSize + cellSize / 4, 
                y * cellSize + cellSize / 4
            )
        self.color = color
        self.size = 32

    def setPosition(self, x: int, y: int, cellSize: int):
        self.position = pygame.Vector2(
            x * cellSize + cellSize / 4, 
            y * cellSize + cellSize / 4
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, (*self.position, self.size, self.size))
