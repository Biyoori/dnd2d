import pygame

class Grid:
    def __init__(self):
        self.cellSize = 64
        self.matrix = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
        ]

    def draw(self, screen: pygame.Surface, cellColor: tuple[int,int,int]) -> None:
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                pygame.draw.rect(screen, cellColor, (x*self.cellSize, y*self.cellSize, self.cellSize-1, self.cellSize-1))