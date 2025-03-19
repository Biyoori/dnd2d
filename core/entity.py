import pygame
import math
from core.grid import Grid

class Entity:
    def __init__(self, color: tuple[int,int,int], movementSpeed: int):
        self.gridX, self.gridY = 0, 0
        self.cellSize = 32
        self.position = pygame.Vector2(0, 0)
            
        self.color = color
        self.size = 32
        self.maxTiles = movementSpeed // 5

        self.dragging = False
        self.startX, self.startY = self.gridX, self.gridY
        self.tempPath = []

    def initialize(self, x: int, y: int, grid: Grid) -> None:
        self.gridX, self.gridY = x, y
        self.cellSize = grid.cellSize
        self.grid = grid
        self.position = pygame.Vector2(
            x * self.cellSize + self.cellSize / 4, 
            y * self.cellSize + self.cellSize / 4
        )

    def setPosition(self, x: int, y: int) -> None:
        self.gridX, self.gridY = x, y
        self.position = pygame.Vector2(
            x * self.cellSize + self.cellSize / 4, 
            y * self.cellSize + self.cellSize / 4
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, (*self.position, self.size, self.size))

    def handleEvent(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if event.button == 1 and self.isHovering(mouseX, mouseY):
                self.dragging = True
                self.startX, self.startY = self.gridX, self.gridY
                self.grid.path = [(self.startX, self.startY)]

            elif event.button == 3 and self.dragging:
                newX = math.floor(event.pos[0] / self.cellSize)
                newY = math.floor(event.pos[1] / self.cellSize)
                if len(self.grid.path) > 1:
                    self.tempPath = (self.grid.path[:-1])
                    self.startX, self.startY = self.grid.path[-1]         

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.position = pygame.Vector2(event.pos) - pygame.Vector2(self.size/2, self.size/2)
            newX = math.floor(event.pos[0] / self.cellSize)
            newY = math.floor(event.pos[1] / self.cellSize)

            tempPath = self.grid.calculatePath((self.startX, self.startY), (newX, newY))

            if len(tempPath) + len(self.tempPath) <= self.maxTiles + 1:
                self.grid.path = self.tempPath + tempPath
                print(self.grid.path)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                self.snapToGrid()

                self.tempPath = []
                self.grid.path = []

    def isHovering(self, mouseX, mouseY):
        return (self.position.x <= mouseX <= self.position.x + self.size and
                self.position.y <= mouseY <=self.position.y + self.size)
    
    def snapToGrid(self):
        if self.isOutOfPath():
            self.setPosition(self.grid.path[0][0], self.grid.path[0][1])
        else:
            lastX, lastY = self.grid.path[-1]
            self.setPosition(lastX, lastY)

    def isOutOfPath(self):
        if not self.grid.path:
            return False
        
        currentX = math.floor(self.position.x / self.cellSize)
        currentY = math.floor(self.position.y / self.cellSize)
        startX, startY = self.grid.path[0]

        distance = max(abs(currentX - startX), abs(currentY - startY))

        return distance > self.maxTiles