from debugging import logger
from typing import TYPE_CHECKING, List, Tuple
import random

if TYPE_CHECKING:
    from core.grid.grid import Grid
    from entities.character.character import Character
    from entities.enemy import Enemy

class DungeonGenerator:
    def __init__(self, grid: "Grid") -> None:
        self._grid= grid

    def generate_rp(self, room_count: int = 5, min_room_size: int = 5, max_room_size = 10) -> List["Room"]:
        self._grid.clear_matrix()
        rooms = []

        while (len(rooms) < room_count):
            room_width = random.randint(min_room_size, max_room_size)
            room_height = random.randint(min_room_size, max_room_size)
            room_x = random.randint(1, self._grid.size[0] - room_width - 1)
            room_y = random.randint(1, self._grid.size[1] - room_height - 1)

            new_room = Room(room_x, room_y, room_width, room_height)

            if any(new_room.intersects(existing_room) for existing_room in rooms):
                continue

            rooms.append(new_room)
            for row in range(room_y, room_y + room_height):
                for col in range(room_x, room_x + room_width):
                    self._grid.set_cell(col, row, 0)

        # Set the room type for each room
        starting_room = random.choice(rooms)
        starting_room.room_type = "start"

        for room in rooms:
            if room.room_type == "start":
                room.cr_budget = 0
            else:
                room.cr_budget = 0.25

        # Connect the rooms with corridors
        self._connect_rooms(rooms)
        
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

        logger.log("Dungeon generated successfully.", "INFO")

    def _get_free_positions(self) -> list[tuple[int, int]]:
        free_positions = []
        for y in range(self._grid._grid_height):
            for x in range(self._grid._grid_width):
                if self._grid.get_cell((x, y)) == 0:
                    free_positions.append((x, y))
        return free_positions

    def spawn_entities(self, player: "Character", enemies: list["Enemy"], rooms: List["Room"]) -> None:
        starting_room = next((room for room in rooms if room.room_type == "start"), None)
        if not starting_room:
            logger.log("No starting room found for spawning entities.", "ERROR")
            return
        
        player_positions = [(x, y) for y in range(starting_room.y, starting_room.y + starting_room.height) 
                            for x in range(starting_room.x, starting_room.x + starting_room.width) 
                            if self._grid.get_cell((x, y)) == 0]
        
        if not player_positions:
            logger.log("No free positions available for spawning player.", "ERROR")
            return
        
        player_pos = random.choice(player_positions)
        player.set_grid_position(player_pos[0], player_pos[1])
        logger.log(f"Player spawned at {player_pos}.", "INFO")

        for room in rooms:
            if room.room_type == "start":
                continue

            room_enemies = []
            remaining_cr = room.cr_budget

            while remaining_cr > 0:
                enemy = random.choice(enemies)
                if enemy.challenge_rating <= remaining_cr:
                    room_enemies.append(enemy)
                    remaining_cr -= enemy.challenge_rating

            for enemy in room_enemies:
                enemy_positions = [(x, y) for y in range(room.y, room.y + room.height)
                                   for x in range(room.x, room.x + room.width)
                                   if self._grid.get_cell((x, y)) == 0]
                
                if not enemy_positions:
                    logger.log("No free positions available for spawning enemies.", "ERROR")
                    continue

                enemy_pos = random.choice(enemy_positions)
                enemy.set_grid_position(enemy_pos[0], enemy_pos[1])
                logger.log(f"Enemy spawned at {enemy_pos}.", "INFO")

class Room:
    def __init__(self, x: int, y: int, width: int, height: int, room_type="normal", cr_budget: float = 1.0) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_type = room_type
        self.cr_budget = cr_budget

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
    
    def contains(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height