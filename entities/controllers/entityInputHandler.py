import pygame
from math import floor

class EntityInputHandler:

    LEFT_MOUSE_BUTTON = 1
    RIGHT_MOUSE_BUTTON = 3

    def __init__(self, entity: "Entity", grid: "Grid", movementController: "EntityMovement"): # type: ignore
        self.entity = entity
        self.grid = grid
        self.movementController = movementController
        self.dragging = False

    def handleEvent(self, event: pygame.event, turnManager: "TurnManager") -> None: # type: ignore
        if not turnManager.isCurrentTurn(self.entity):
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.onMouseDown(event)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.onMouseMove(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.onMouseUp(turnManager)

    def onMouseDown(self, event: pygame.event) -> None:        
        if event.button == self.LEFT_MOUSE_BUTTON and self.isMouseOverEntity(*event.pos):
            self.dragging = True
            print(self.entity.gridPosition, *self.entity.gridPosition)
            self.movementController.startMovement(*self.entity.gridPosition)

        elif event.button == self.RIGHT_MOUSE_BUTTON and self.dragging:
            self.entity.pathfinder.updatePath()               

    def onMouseMove(self, event: pygame.event) -> None:
        self.entity.position = pygame.Vector2(event.pos) - pygame.Vector2(self.entity.size/2, self.entity.size/2)
        newX = floor(event.pos[0] / self.grid.cellSize)
        newY = floor(event.pos[1] / self.grid.cellSize)
        self.movementController.updateMovement(newX, newY)

    def onMouseUp(self, turnManager: "TurnManager") -> None: #type: ignore
        if self.dragging:
            self.dragging = False
            self.movementController.finalizeMovement(turnManager)

    def isMouseOverEntity(self, mouseX: int, mouseY: int) -> bool:
        return (self.entity.position.x <= mouseX <= self.entity.position.x + self.entity.size and
                self.entity.position.y <= mouseY <= self.entity.position.y + self.entity.size)