from typing import TYPE_CHECKING
from .debug_logger import logger

if TYPE_CHECKING:
    from entity_manager import GameEntityManager

class DebugConsole:
    def __init__(self, entity_manager: "GameEntityManager") -> None:
        self.entity_manager = entity_manager

    def handle_command(self, command: str) -> None:
        if command.startswith("teleport"):
            _, x, y = command.split()
            self.entity_manager.get_character().set_grid_position(int(x), int(y))
            logger.log(f"teleported to ({x}, {y})", "DEBUG")