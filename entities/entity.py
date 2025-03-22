import pygame
from entities.controllers.entityPathfinder import EntityPathfinder
from entities.controllers.movementController import EntityMovement
from entities.controllers.entityInputHandler import EntityInputHandler
from entities.entityRenderer import EntityRenderer

class Entity:
    def __init__(self, color: tuple[int,int,int], movementSpeed: int):
        self._gridX, self._gridY = 0, 0
        self._position = pygame.Vector2(0, 0)    
        self.color = color
        self._size = 32
        self._maxTiles = movementSpeed // 5

    @property
    def gridPosition(self) -> list[int, int]:
        return [self._gridX, self._gridY]
    
    def setGridPosition(self, x: int, y: int):
        self._gridX, self._gridY = x, y

    @property
    def size(self) -> int:
        return self._size
    
    @property
    def maxTiles(self) -> int:
        return self._maxTiles
    
    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, newPosition: pygame.Vector2) -> None:
        self._position = newPosition

    def initialize(self, x: int, y: int, grid: "Grid", movementManager: "MovementManager") -> None: # type: ignore
        self.setGridPosition(x, y)
        self._size = grid.cellSize // 2
        self.setPosition(grid)

        self.pathfinder = EntityPathfinder(grid)
        self.movement = EntityMovement(self, grid, movementManager, self.pathfinder)
        self.inputHandler = EntityInputHandler(self, grid, self.movement)
        self.renderer = EntityRenderer(self, grid)
        
    def setPosition(self, grid: "Grid") -> None: # type: ignore
        self.position = pygame.Vector2(
            self._gridX * grid.cellSize + grid.cellSize / 4, 
            self._gridY * grid.cellSize + grid.cellSize / 4
        )

    def update(self, event: pygame.event, turnManager: "TurnManager") -> None:  # type: ignore
        self.inputHandler.handleEvent(event, turnManager)

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.draw(surface)
    
    