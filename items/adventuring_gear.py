from typing import Callable
from items.item import Item


class AdventuringGear(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, consumable: bool = False, container: bool = False, capacity: int = 0) -> None:
        super().__init__(name, description, "adventuring_gear", weight, value, consumable)
        self.container = container
        self.contents = [] if container else None
        self.max_capacity = capacity if container else None

    def __str__(self) -> str:
        return f"{self.name}: {self.weight}lb, {self.value}gp - {self.description}"