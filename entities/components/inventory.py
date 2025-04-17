from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from items.item import Item

@dataclass(frozen=True)
class InventoryData:
    items: List["Item"] = field(default_factory=list)

class InventorySystem:
    def __init__(self, data: InventoryData) -> None:
        self._data = data
    
    @property
    def items(self) -> List["Item"]:
        return list(self._data.items)

    def add_item(self, item: "Item") -> InventoryData:
        new_items = self._data.items + [item]
        self._data = InventoryData(items=new_items)
        print(f"Added {item.name} to inventory.")
        return self._data

    def remove_item(self, item_name: str) -> InventoryData:
        new_items = [item for item in self._data.items if item.name != item_name]

        if len(new_items) == len(self._data.items):
            print(f"There's no such item as {item_name} in inventory.")
        else:
            print(f"Deleted {item_name} from inventory.")

        self._data = InventoryData(items=new_items)
        return self._data
            
    def show_inventory(self) -> None:
        if not self._data.items:
            print("Inventory is empty")
            return

        print("\n📜 **Inventory:**")
        for item in self._data.items:
            print(f"- {item}")

    @property
    def is_empty(self) -> bool:
        return len(self._data.items) == 0
    
    def get_inventory(self) -> List["Item"]:
        return self._data.items.copy()