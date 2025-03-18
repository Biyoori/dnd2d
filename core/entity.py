import pygame
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

    def initialize(self, x: int, y: int, grid: Grid):
        self.gridX, self.gridY = x, y
        self.cellSize = grid.cellSize
        self.grid = grid
        self.position = pygame.Vector2(
            x * self.cellSize + self.cellSize / 4, 
            y * self.cellSize + self.cellSize / 4
        )

    def setPosition(self, x: int, y: int):
        self.gridX, self.gridY = x, y
        self.position = pygame.Vector2(
            x * self.cellSize + self.cellSize / 4, 
            y * self.cellSize + self.cellSize / 4
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, (*self.position, self.size, self.size))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if self.isHovering(mouseX, mouseY):
                self.dragging = True
                self.startX, self.startY = self.gridX, self.gridY

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.position = pygame.Vector2(event.pos) - pygame.Vector2(self.size/2, self.size/2)

                newX = round(self.position.x / self.cellSize)
                newY = round(self.position.y / self.cellSize)

                self.grid.updatePath((self.startX, self.startY), (newX, newY), self.maxTiles * 5)
                print(self.grid.path)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                self.snapToGrid()

                self.grid.path = []

    def isHovering(self, mouseX, mouseY):
        return (self.position.x <= mouseX <= self.position.x + self.size and
                self.position.y <= mouseY <=self.position.y + self.size)
    
    def snapToGrid(self):
        newX = round(self.position.x / self.cellSize)
        newY = round(self.position.y / self.cellSize)

        dx = abs(newX - self.startX)
        dy = abs(newY - self.startY)

        distance = max(dx, dy)

        if distance <= self.maxTiles:
            self.setPosition(newX, newY)
        else:
            self.setPosition(self.startX, self.startY)
