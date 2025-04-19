from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from core.grid.grid import Grid
    from entities.character.character import Character
    from entities.enemy import Enemy

class DungeonGenerator:
    def __init__(self, grid: "Grid") -> None:
        self._grid= grid
    
    def generate(self) -> None:
        self._grid.clear_matrix()
       
        start_x = random.randint(1, self._grid._grid_width - 2)
        start_y = random.randint(1, self._grid._grid_height - 2)
        self._grid.set_cell(start_x, start_y, 0)

        current_x, current_y = start_x, start_y
        for _ in range(self._grid._grid_width * self._grid._grid_height // 4):
            direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            new_x = max(1, min(self._grid._grid_width - 2, current_x + direction[0]))
            new_y = max(1, min(self._grid._grid_height - 2, current_y + direction[1]))
            self._grid.set_cell(new_x, new_y, 0)
            current_x, current_y = new_x, new_y

        print("[DEBUG] Dungeon generated successfully.")

    def _get_free_positions(self) -> list[tuple[int, int]]:
        free_positions = []
        for y in range(self._grid._grid_height):
            for x in range(self._grid._grid_width):
                if self._grid.get_cell((x, y)) == 0:
                    free_positions.append((x, y))
        return free_positions

    def spawn_entities(self, player: "Character", enemies: list["Enemy"]) -> None:
        free_positions = self._get_free_positions()
        print(free_positions)
        if not free_positions:
            print("[DEBUG] No free positions available for spawning entities.")
            return
        
        player_pos = random.choice(free_positions)
        free_positions.remove(player_pos)
        player.set_grid_position(player_pos[0], player_pos[1])
        print(f"[DEBUG] Player spawned at {player_pos}.")

        for enemy in enemies:
            if not free_positions:
                print("[DEBUG] No free positions available for spawning enemies.")
                break
            enemy_pos = random.choice(free_positions)
            free_positions.remove(enemy_pos)
            enemy.set_grid_position(enemy_pos[0], enemy_pos[1])
            print(f"[DEBUG] Enemy spawned at {enemy_pos}.")
            enemy.set_grid_position(enemy_pos[0], enemy_pos[1])