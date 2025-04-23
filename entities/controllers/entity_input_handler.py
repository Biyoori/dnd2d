import pygame
from math import floor
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from core.grid.grid import Grid
    from entities.entity import Entity
    from entities.controllers.movement_controller import EntityMovement
    from combat.turn_manager import TurnManager

class EntityInputHandler:
    LEFT_MOUSE_BUTTON = 1
    RIGHT_MOUSE_BUTTON = 3

    def __init__(self, entity: "Entity", grid: "Grid", movement_controller: "EntityMovement") -> None:
        self.entity = entity
        self.grid = grid
        self.movement_controller = movement_controller
        self.dragging = False

    def handle_event(self, event: pygame.event, turn_manager: "TurnManager", mouse_pos: Tuple[int, int]) -> None:
        if not turn_manager.is_current_turn(self.entity):
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Mouse button down at {mouse_pos}")
            self._handle_mouse_down(event, mouse_pos)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._handle_mouse_move(event, mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == self.LEFT_MOUSE_BUTTON:
            self._handle_mouse_up(turn_manager)

    def _handle_mouse_down(self, event: pygame.event, mouse_pos: Tuple[int, int]) -> None:   
        if not hasattr(event, "pos"):
            return

        if event.button == self.LEFT_MOUSE_BUTTON and self._is_mouse_over_entity(*mouse_pos):
            self.dragging = True
            self.movement_controller.start_movement(*self.entity.grid_position)
        elif event.button == self.RIGHT_MOUSE_BUTTON and self.dragging:
            self.entity.pathfinder.break_path()               

    def _handle_mouse_move(self, event: pygame.event, mouse_pos: Tuple[int, int]) -> None:
        if not hasattr(event, "pos"):
            return
        
        self.entity.position = pygame.Vector2(mouse_pos) - pygame.Vector2(self.entity.size/2, self.entity.size/2)
        grid_x = floor(mouse_pos[0] / self.grid.cell_size)
        grid_y = floor(mouse_pos[1] / self.grid.cell_size)
        self.movement_controller.update_movement(grid_x, grid_y)

    def _handle_mouse_up(self, turn_manager: "TurnManager") -> None:
        if self.dragging:
            self.dragging = False
            self.movement_controller.finalize_movement(turn_manager)

    def _is_mouse_over_entity(self, mouse_x: int, mouse_y: int) -> bool:
        return (self.entity.position.x <= mouse_x <= self.entity.position.x + self.entity.size and
                self.entity.position.y <= mouse_y <= self.entity.position.y + self.entity.size)