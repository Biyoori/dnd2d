class Item:
    def __init__(self, name: str, description: str, weight: float, value: int, consumable: bool = False):
        self.name = name
        self.description = description
        self.weight = weight
        self.value = value
        self.consumable = consumable

    def use(self, character):
        print(f"{character.name} can't use {self.name}.")

    def __str__(self):
        return f"{self.name}: {self.weight}lb, {self.value}gp - {self.description}"