from typing import TYPE_CHECKING
from items.weapon import Weapon

if TYPE_CHECKING:
    from entities.components.inventory import InventorySystem
    
class WeaponSystem:
    def __init__(self, inventory: "InventorySystem") -> None:
        self.inventory = inventory
        self.equipped_weapon: Weapon | None = None

    def equip_weapon(self, weapon_name) -> None:
        for item in self.inventory.items:
            if isinstance(item, Weapon) and item.name == weapon_name:
                self.equipped_weapon = item
                print(f"Equipped {item.name}")
                return
        print(f"No such weapon in in inventory: {weapon_name}")

    def get_equipped_weapon(self) -> Weapon | None:
        return self.equipped_weapon

    def unequip_weapon(self):
        if self.equipped_weapon:
            print(f"Unequipped item {self.equipped_weapon.name}")
            self.equipped_weapon = None
        else:
            print(f"No weapon is currently equipped")

    def equip_weapon_directly(self, weapon: "Weapon") -> None:
        self.equipped_weapon = weapon