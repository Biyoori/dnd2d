from typing import TYPE_CHECKING, Tuple

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

    def find_path_a_star(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> list[tuple[int, int]]:
        # Implement A* pathfinding algorithm
        from heapq import heappop, heappush

        open_set = []
        heappush(open_set, (0, start_pos))

        came_from = {}
        g_score = {start_pos: 0}
        f_score = {start_pos: self.heuristic(start_pos, end_pos)}

        while open_set:
            _, current = heappop(open_set)

            if current == end_pos:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_pos)
                return path[::-1]
            
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if not self.grid.is_valid(neighbor):
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end_pos)
                    heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No path found

    def heuristic(self, a: Tuple[int,int], b: Tuple[int,int]) -> int:
        # Heuristic: Chebyshev distance
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))