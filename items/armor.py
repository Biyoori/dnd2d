from items.item import Item

class Armor(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, armor_type: str, armor_class: int) -> None:
        super().__init__(name, description, weight, value)
        self.armor_type = armor_type
        self.armor_class = armor_class

    def __str__(self) -> str:
        return f"{self.name}: {self.weight}lb. {self.value}gp - {self.armor_type}, {self.armor_tlass} | {self.description}"