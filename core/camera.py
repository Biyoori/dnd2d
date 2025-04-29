from typing import Tuple
from pygame import Vector2


class Camera:
    def __init__(self) -> None:
        self.offset_x = 0
        self.offset_y = 0
        self.speed = 10

    @property
    def offset(self) -> Tuple[int, int]:
        return self.offset_x, self.offset_y    

    def move(self, dx: int, dy: int) -> None:
        self.offset_x += dx
        self.offset_y += dy

    def apply_offset(self, mouse_pos: Tuple[int, int]) -> tuple[int, int]:
        grid_x = mouse_pos[0] - self.offset_x
        grid_y = mouse_pos[1] - self.offset_y

        return (int(grid_x), int(grid_y))