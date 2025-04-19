from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.grid.grid import Grid

class Pathfinding:
    def __init__(self, grid: "Grid") -> None:
        self.grid = grid

    def find_path(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> list[tuple[int, int]]:
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        calculated_path = []

        delta_x = abs(end_x - start_x)
        delta_y = abs(end_y - start_y)

        step_x = 1 if start_x < end_x else -1
        step_y = 1 if start_y < end_y else -1
        
        error = delta_x - delta_y

        while end_x != start_x or end_y != start_y:
            calculated_path.append((start_x, start_y))
            doubled_error = 2 * error

            if doubled_error > -delta_y:
                error -= delta_y
                start_x += step_x

            if doubled_error < delta_x:
                error += delta_x
                start_y += step_y

        calculated_path.append((end_x, end_y))   
        return calculated_path

    #def heuristic(self, a, b):
        # Implement heuristic function for pathfinding
        #pass