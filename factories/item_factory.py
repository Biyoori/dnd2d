from items.weapon import Weapon
from items.armor import Armor
from items.potion import Potion
from items.adventuring_gear import AdventuringGear

import json

class ItemFactory:
    _loaded_types = {}
    _cache = {}
    
    _item_files = {
        "weapons": "data/items/weapons/weapons.json",
        "armors": "data/items/armor/armor.json",
        "potions": "data/items/potions/potions.json",
        "adventuring_gear": "data/items/other/other.json"
    }

    @staticmethod
    def create(name: str):
        if name in ItemFactory._cache:
            return ItemFactory._cache[name]
        
        for type_name, file_path in ItemFactory._item_files.items():
            if type_name not in ItemFactory._loaded_types:
                with open(file_path, "r") as file:
                    ItemFactory._loaded_types[type_name] = json.load(file)

            items = ItemFactory._loaded_types[type_name]
            if name in items:
                item_data = items[name]
                item = ItemFactory._build_item(name, item_data)
                ItemFactory._cache[name] = item
                return item
        
        raise ValueError(f"Item '{name}' not found in any item type")

    @staticmethod
    def _build_item(name: str, data: dict) -> Weapon | Armor | Potion | AdventuringGear:
        type_ = data.get("type")
        if type_ == 'weapon':
            return Weapon(
                name=name, 
                description=data["description"], 
                weight=data["weight"], 
                value=data["value"], 
                weapon_type=data["weapon_type"], 
                damage=data["damage"], 
                damage_type=data["damage_type"], 
                properties=data["properties"]
            )
        elif type_ == 'armor':
            return Armor(
                name=name, 
                description=data["description"], 
                weight=data["weight"], 
                value=data["value"], 
                armor_class=data["armor_class"], 
                armor_type=data["armor_type"]
            )
        elif type_ == 'potion':
            return Potion(
                name=name, 
                description=data["description"], 
                weight=data["weight"], 
                value=data["value"], 
                effect=data["effect"]
            )
        elif type_ == 'adventuring_gear':
            return AdventuringGear(
                name=name, 
                description=data["description"], 
                weight=data["weight"], 
                value=data["value"], 
                consumable=data.get("consumable", False), 
                container=data.get("container", False), 
                capacity=data.get("capacity", 0)
            )
        else:
            raise ValueError("Unknown item type")