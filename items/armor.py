from items.item import Item

class Armor(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, armorType: str, armorClass: int):
        super().__init__(name, description, weight, value)
        self.armorType = armorType
        self.armorClass = armorClass

    def __str__(self):
        return f"{self.name}: {self.weight}lb. {self.value}gp - {self.armorType}, {self.armorClass} | {self.description}"