from items.item import Item
from typing import List

class Weapon(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, weapon_type: str, damage: str, damage_type: str, properties: List[str], finesse: bool = False, attack_range: int = 5) -> None:
        super().__init__(name, description, "weapon", weight, value)
        self.weapon_type = weapon_type
        self.finesse = finesse
        self.damage = damage
        self.damage_type = damage_type
        self.properties = properties
        self.range = attack_range

    def __str__(self) -> str:
        return f"{self.name}: {self.weight}lb. {self.value}gp - {self.weapon_type}, {self.damage}, {self.description}"