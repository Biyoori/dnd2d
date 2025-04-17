from typing import TYPE_CHECKING
from core.event import Event
from items.weapon import Weapon
from ui.game_console import console

if TYPE_CHECKING:
    from entities.components.inventory import InventorySystem
    
class WeaponSystem:
    def __init__(self, inventory: "InventorySystem") -> None:
        self.unarmed_strike = Weapon("Unarmed Strike", "Unarmed strike", 0, 0, "Unarmed", "1d4", "Bludgeoning", [], False, 5)
        self.inventory = inventory
        self.equipped_weapon = self.unarmed_strike

        Event.subscribe("equip_weapon", self.equip_weapon_directly)

    def equip_weapon(self, weapon_name) -> None:
        for item in self.inventory.items:
            if isinstance(item, Weapon) and item.name == weapon_name:
                self.equipped_weapon = item
                console.log(f"Equipped {item.name}")
                return
        console.log(f"No such weapon in in inventory: {weapon_name}")

    def get_equipped_weapon(self) -> Weapon | None:
        return self.equipped_weapon

    def unequip_weapon(self):
        if self.equipped_weapon:
            console.log(f"Unequipped item {self.equipped_weapon.name}")
            self.equipped_weapon = self.unarmed_strike
        else:
            console.log(f"No weapon is currently equipped")

    def equip_weapon_directly(self, weapon: "Weapon") -> None:
        self.equipped_weapon = weapon