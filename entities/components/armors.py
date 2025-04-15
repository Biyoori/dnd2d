
from typing import TYPE_CHECKING
from items.armor import Armor

if TYPE_CHECKING:
    from entities.components.inventory import InventorySystem

class ArmorSystem:
    def __init__(self, inventory: "InventorySystem") -> None:
        self.equipped_armor = None
        self.equipped_shield = None

    def equip_armor(self, armor_name: str) -> None:
        for item in self.inventory.items:
            if isinstance(item, Armor) and item.name == armor_name:
                self.equipped_armor = item
                print(f"Equipped {item.name}")
                return
        print(f"No such armor in inventory: {armor_name}")

    def unequip_armor(self) -> None:
        if self.equipped_armor:
            print(f"Unequipped {self.equipped_armor.name}")
            self.equipped_armor = None
        else:
            print("No armor equipped")

    def get_equipped_armor(self) -> Armor | None:
        return self.equipped_armor