import pygame
from settings import getColorFromPallette

class Grid:
    def __init__(self, size: int = 10, cellSize: int = 64):
        self._cellSize = cellSize
        self._size = size
        self._matrix = [[0 for _ in range(size)] for _ in range(size)]
        self._navigationPath: list[tuple[int, int]] = []

    @property
    def cellSize(self) -> int:
        return self._cellSize
    
    def size(self) -> int:
        return self._size
    
    @property
    def navigationPath(self) -> list[tuple[int, int]]:
        return self._navigationPath.copy()
    
    @navigationPath.setter
    def navigationPath(self, newPath: list[tuple[int, int]]) -> None:
        self._navigationPath = newPath

    def calculatePath(self, startPos: tuple[int, int], endPos: tuple[int, int]) -> list[tuple[int, int]]:
        startX, startY = startPos
        endX, endY = endPos
        calculatedPath = []

        deltaX = abs(endX - startX)
        deltaY = abs(endY - startY)

        stepX = 1 if startX < endX else -1
        stepY = 1 if startY < endY else -1
        
        error = deltaX - deltaY

        while endX != startX or endY != startY:
            calculatedPath.append((startX, startY))
            doubledError = 2 * error

            if doubledError > -deltaY:
                error -= deltaY
                startX += stepX

            if doubledError < deltaX:
                error += deltaX
                startY += stepY

        calculatedPath.append((endX, endY))   
        return calculatedPath
    
    def draw(self, screen: pygame.Surface) -> None:
        gray = getColorFromPallette("gray")
        green = getColorFromPallette("green")

        for row, gridRow in enumerate(self._matrix):
            for col, _ in enumerate(gridRow):
                cellColor = green if (col, row) in self._navigationPath else gray    
                pygame.draw.rect(screen, cellColor, (col*self.cellSize, row*self.cellSize, self.cellSize-1, self.cellSize-1))