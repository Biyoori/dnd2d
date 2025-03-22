from items.item import Item

class Weapon(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, weaponType: str, damage: str):
        super().__init__(name, description, weight, value)
        self.weaponType = weaponType
        self.damage = damage

    def attack(self):
        print(f"You attack using {self.name}, dealing {self.damage} points of damage")

    def __str__(self):
        return f"{self.name}: {self.weight}lb. {self.value}gp - {self.weaponType}, {self.damage}, {self.description}"