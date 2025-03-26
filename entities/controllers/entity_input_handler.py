import pygame
from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.grid import Grid
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

    def handle_event(self, event: pygame.event, turn_manager: "TurnManager") -> None:
        if not turn_manager.is_current_turn(self.entity):
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_down(event)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.on_mouse_move(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == self.LEFT_MOUSE_BUTTON:
            self.on_mouse_up(turn_manager)

    def on_mouse_down(self, event: pygame.event) -> None:        
        if event.button == self.LEFT_MOUSE_BUTTON and self.is_mouse_over_entity(*event.pos):
            self.dragging = True
            self.movement_controller.start_movement(*self.entity.grid_position)

        elif event.button == self.RIGHT_MOUSE_BUTTON and self.dragging:
            self.entity.pathfinder.update_path()               

    def on_mouse_move(self, event: pygame.event) -> None:
        self.entity.position = pygame.Vector2(event.pos) - pygame.Vector2(self.entity.size/2, self.entity.size/2)
        new_x = floor(event.pos[0] / self.grid.cell_size)
        new_y = floor(event.pos[1] / self.grid.cell_size)
        self.movement_controller.update_movement(new_x, new_y)

    def on_mouse_up(self, turn_manager: "TurnManager") -> None:
        if self.dragging:
            self.dragging = False
            self.movement_controller.finalize_movement(turn_manager)

    def is_mouse_over_entity(self, mouse_x: int, mouse_y: int) -> bool:
        return (self.entity.position.x <= mouse_x <= self.entity.position.x + self.entity.size and
                self.entity.position.y <= mouse_y <= self.entity.position.y + self.entity.size)