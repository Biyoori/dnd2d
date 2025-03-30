from typing import Tuple
import math

class MenuPositioning:
    def __init__(self) -> None:
        self._position = None
        self.radius = 60
        self.sector_offset = 90
        self.sectors = 6

    @property
    def position(self) -> Tuple[int, int]:
        return self._position
    
    @position.setter
    def position(self, value: Tuple[int, int]) -> None:
        self._position = value

    def calculate_position(self, index: int) -> Tuple[float]:
        angle = math.radians(index * (360 / self.sectors) + self.sector_offset)

        x = self.position[0] + self.radius * math.cos(angle)
        y = self.position[1] + self.radius * math.sin(angle)
            
        return (x, y)