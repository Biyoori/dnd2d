import pygame
from math import floor

class EntityMovement:
    def __init__(self, entity: "Entity", grid: "Grid", movementManager: "MovementManager", pathfinder: "EntityPathfinder"): #type: ignore
        self.entity = entity
        self.grid = grid
        self.movementManager = movementManager
        self.pathfinder = pathfinder

    def startMovement(self, pathStartX: int, pathStartY: int) -> None:
        self.pathfinder.startMovement(pathStartX, pathStartY)
        self.movementUsed = 0

    def updateMovement(self, newX: int, newY: int) -> None:
        newPath = self.pathfinder.calculatePath(newX, newY)

        if self.movementManager.canMove(self.entity, len(self.pathfinder.tempPath) + len(newPath) - 1):
            self.grid.navigationPath = self.pathfinder.tempPath + newPath

    def finalizeMovement(self, turnManager: "TurnManager") -> None: #type: ignore
        self.snapToGrid()
        self.movementManager.registerMovement(self.entity, len(self.grid.navigationPath) - 1, turnManager)
        self.pathfinder.clearPath()

    def snapToGrid(self) -> None:
        if self.isOutOfPath():
            self.setPosition(self.grid.navigationPath[0][0], self.grid.navigationPath[0][1])
        else:
            lastX, lastY = self.grid.navigationPath[-1]
            self.setPosition(lastX, lastY)

    def isOutOfPath(self) -> bool:
        if not self.grid.navigationPath:
            return False
        
        currentX = floor(self.entity.position.x / self.grid.cellSize)
        currentY = floor(self.entity.position.y / self.grid.cellSize)
        pathStartX, pathStartY = self.grid.navigationPath[0]

        distance = max(abs(currentX - pathStartX), abs(currentY - pathStartY))

        return distance > self.entity.maxTiles
    
    def setPosition(self, x: int, y: int) -> None:
        self.entity.setGridPosition(x, y)
        self.entity.position = pygame.Vector2(
            x * self.grid.cellSize + self.grid.cellSize / 4, 
            y * self.grid.cellSize + self.grid.cellSize / 4
        )