import pygame
from entities.controllers.entity_pathfinder import EntityPathfinder
from entities.controllers.movement_controller import EntityMovement
from entities.controllers.entity_input_handler import EntityInputHandler
from entities.entity_renderer import EntityRenderer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.components.factions import Faction

if TYPE_CHECKING:
    from core.grid.grid import Grid
    from movement.movement_manager import MovementManager
    from combat.turn_manager import TurnManager

class Entity:
    def __init__(self, color: tuple[int,int,int], movement_speed: int, faction: "Faction") -> None:
        self._grid_x, self._grid_y = 0, 0
        self._position = pygame.Vector2(0, 0)    
        self.color = color
        self._size = 32
        self._max_tiles = movement_speed // 5
        self.faction = faction

    @property
    def grid_position(self) -> list[int, int]:
        return [self._grid_x, self._grid_y]
    
    def set_grid_position(self, x: int, y: int) -> None:
        self._grid_x, self._grid_y = x, y

    @property
    def size(self) -> int:
        return self._size
    
    @property
    def max_tiles(self) -> int:
        return self._max_tiles
    
    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, new_position: pygame.Vector2) -> None:
        self._position = new_position

    def initialize(self, x: int, y: int, grid: "Grid", movement_manager: "MovementManager") -> None:
        self.set_grid_position(x, y)
        self._size = grid.cell_size // 2
        self.set_position(grid)

        self.pathfinder = EntityPathfinder(self, grid, movement_manager)
        self.movement = EntityMovement(self, grid, movement_manager, self.pathfinder)
        self.input_handler = EntityInputHandler(self, grid, self.movement)
        self.renderer = EntityRenderer(self, grid)
        
    def set_position(self, grid: "Grid") -> None:
        self._position = pygame.Vector2(
            self._grid_x * grid.cell_size + grid.cell_size / 4, 
            self._grid_y * grid.cell_size + grid.cell_size / 4
        )

    def update(self, event: pygame.event, turn_manager: "TurnManager") -> None:
        self.input_handler.handle_event(event, turn_manager)

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.draw(surface)

    def update_size(self, grid) -> None:
        self._size = grid.cell_size // 2