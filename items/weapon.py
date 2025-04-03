from items.item import Item

class Weapon(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, weapon_type: str, damage: str, damage_type: str, finesse:bool = False, range: int = 5) -> None:
        super().__init__(name, description, weight, value)
        self.weapon_type = weapon_type
        self.finesse = finesse
        self.damage = damage
        self.damage_type = damage_type
        self.range = range

    def attack(self) -> None:
        print(f"You attack using {self.name}, dealing {self.damage} points of damage")

    def __str__(self) -> str:
        return f"{self.name}: {self.weight}lb. {self.value}gp - {self.weapon_type}, {self.damage}, {self.description}"