from re import split
from turtle import width
from typing import TYPE_CHECKING, List, Tuple
import random

if TYPE_CHECKING:
    from core.grid.grid import Grid
    from entities.character.character import Character
    from entities.enemy import Enemy

class DungeonGenerator:
    def __init__(self, grid: "Grid") -> None:
        self._grid= grid
    
    def generate_bsp(self, room_count: int = 5, min_room_size: int = 5) -> List["Room"]:
        self._grid.clear_matrix()
        spaces = self._split_space(0, 0, self._grid.size[0], self._grid.size[1], min_room_size)

        rooms = self._generate_rooms(spaces, min_room_size)

        self._connect_rooms(rooms)

        print("[DEBUG] Dungeon generated successfully.")
        print("[DEBUG] Rooms generated:")
        for room in rooms:
            print(f"[DEBUG] Room at ({room.x}, {room.y}) with size ({room.width}, {room.height})")
        return rooms

    def _split_space(self, x: int, y: int, width: int, height: int, min_size: int) -> List[Tuple[int, int, int, int]]:
        if width < min_size * 2 and height < min_size * 2: 
            return [(x, y, width, height)]
        
        split_horizontally = random.choice([True, False])

        if width < height and width >= min_size * 2:
            split_horizontally = False
        elif height < width and height >= min_size * 2:
            split_horizontally = True

        if split_horizontally:
            if height < min_size * 2:
                return [(x, y, width, height)]
            split = random.randint(min_size, height - min_size)
            return (self._split_space(x, y, width, split, min_size) +
                    self._split_space(x, y + split, width, height - split, min_size))
        else:
            if width < min_size * 2:
                return [(x, y, width, height)]
            split = random.randint(min_size, width - min_size)
            return (self._split_space(x, y, split, height, min_size) +
                    self._split_space(x + split, y, width - split, height, min_size))
        
    def _generate_rooms(self, spaces: List[Tuple[int, int, int, int]], min_room_size: int, room_buffer: int = 1) -> List[Tuple[int, int, int, int]]:
        rooms = []
        for x, y, width, height in spaces:

            if width < min_room_size or height < min_room_size:
                continue

            room_width = random.randint(min_room_size, width)
            room_height = random.randint(min_room_size, height)
            room_x = random.randint(x, x + width - room_width)
            room_y = random.randint(y, y + height - room_height)

            new_room = Room(room_x, room_y, room_width, room_height)

            if any(new_room.intersects_with_buffer(existing_room, room_buffer) for existing_room in rooms):
                continue

            rooms.append(new_room)

            for row in range(room_y, room_y + room_height):
                for col in range(room_x, room_x + room_width):
                    self._grid.set_cell(col, row, 0)

        return rooms
    
    def _connect_rooms(self, rooms: List["Room"]) -> None:
        for i in range(len(rooms) - 1):
            room_a = rooms[i]
            room_b = rooms[i + 1]

            center_a = room_a.get_center()
            center_b = room_b.get_center()

            if center_a[0] != center_b[0]:
                for x in range(min(center_a[0], center_b[0]), max(center_a[0], center_b[0]) + 1):
                    self._grid.set_cell(x, center_a[1], 0)

            if center_a[1] != center_b[1]:
                for y in range(min(center_a[1], center_b[1]), max(center_a[1], center_b[1]) + 1):
                    self._grid.set_cell(center_b[0], y, 0)

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

class Room:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    def intersects(self, other: "Room") -> bool:
        return not (self.x + self.width < other.x or
                    self.x > other.x + other.width or
                    self.y + self.height < other.y or
                    self.y > other.y + other.height)
    
    def intersects_with_buffer(self, other: "Room", buffer: int) -> bool:
        return not (self.x + self.width + buffer < other.x or
                    self.x > other.x + other.width + buffer or
                    self.y + self.height + buffer < other.y or
                    self.y > other.y + other.height + buffer)