import pygame
from core.settings import COLOR_PALETTE

class Grid:
    def __init__(self):
        self.cellSize = 64
        self.matrix = [[0 for _ in range(10)] for _ in range(10)]
        self.path = []

    def calculatePath(self, startPos: pygame.Vector2, endPos: pygame.Vector2) -> list[pygame.Vector2]:
        startX, startY = startPos
        endX, endY = endPos
        path = []

        deltaX = abs(endX - startX)
        deltaY = abs(endY - startY)

        stepX = 1 if startX < endX else -1
        stepY = 1 if startY < endY else -1
        
        error = deltaX - deltaY

        while(endX != startX or endY != startY):
            path.append((startX, startY))
            doubledError = 2 * error

            if doubledError > -deltaY:
                error -= deltaY
                startX += stepX

            if doubledError < deltaX:
                error += deltaX
                startY += stepY

        path.append((endX, endY))   
        return path
    
    def draw(self, screen: pygame.Surface) -> None:
        for y, row in enumerate(self.matrix):
            for x, _ in enumerate(row):
                cellColor = COLOR_PALETTE["gray"]
                if (x, y) in self.path:
                    cellColor = COLOR_PALETTE["green"]
                pygame.draw.rect(screen, cellColor, (x*self.cellSize, y*self.cellSize, self.cellSize-1, self.cellSize-1))