from ui.game_console import console

class Item:
    def __init__(self, name: str, description: str, item_type: str, weight: float, value: int, consumable: bool = False) -> None:
        self.name = name
        self.description = description
        self.weight = weight
        self.value = value
        self.consumable = consumable
        self.item_type = item_type

    def use(self, character) -> None:
        console.log(f"{character.name} can't use {self.name}.")

    def __str__(self) -> str:
        return f"{self.name}: {self.weight}lb, {self.value}gp - {self.description}"