from encodings.punycode import T
from typing import Tuple


class Camera:
    def __init__(self, screen_width: int, screen_height: int, layer_width: int, layer_height: int) -> None:
        self.layer_width = layer_width
        self.layer_height = layer_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 5
        self.offset_x = 0
        self.offset_y = 0

    def move(self, dx: int, dy: int) -> None:
        """Move the camera by dx and dy."""
        self.offset_x += dx * self.speed
        self.offset_y += dy * self.speed
    
    def apply(self, position: Tuple[int, int]) -> Tuple[int, int]:
        x,y = position
        return x - self.offset_x, y - self.offset_y
    
    def get_offset(self) -> Tuple[int, int]:
        """Get the current offset of the camera."""
        return self.offset_x, self.offset_y