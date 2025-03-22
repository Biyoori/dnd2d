from items.item import Item

class Potion(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, effect: str, potency: int):
        super().__init__(name, description, weight, value, consumable=True)

    def use(self, character):
        print(f"{character.name}, used {self.name} {self.effect} {self.potency} points!")

    def __str__(self):
        return f"{self.name}: {self.weight}lb. {self.value}gp - Effect: {self.effect}, Potency {self.potency} | {self.description}"