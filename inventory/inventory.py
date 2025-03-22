from items.item import Item

class Inventory:
    def __init__(self):
        self.items = []

    def addItem(self, item: Item):
        self.items.append(item)
        print(f"Added {item.name} to inventory.")

    def removeItem(self, itemName: str):
        for item in self.items:
            if itemName == item.name:
                self.items.remove(item)
                print(f"Deleted {item.name} from inventory.")
                return
            print(f"There's no such item as {item.name} in inventory.")

    def showInventory(self):
        if not self.items:
            print("Inventory is empty")
            return

        print("\n📜 **Inventory:**")
        for item in self.items:
            print(f"- {item}")