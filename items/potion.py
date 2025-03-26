from items.item import Item

class Potion(Item):
    def __init__(self, name: str, description: str, weight: float, value: int, effect: str, potency: int) -> None:
        super().__init__(name, description, weight, value, consumable=True)
        self.effect = effect
        self.potency = potency

    def use(self, character) -> None:
        print(f"{character.name}, used {self.name} {self.effect} {self.potency} points!")

    def __str__(self) -> str:
        return f"{self.name}: {self.weight}lb. {self.value}gp - Effect: {self.effect}, Potency {self.potency} | {self.description}"