import random
from collections import deque

class Combat:
    def __init__(self, characters, enemies, turnManager):
        self.characters = characters
        self.combatants = characters + enemies
        self.turnQueue = deque(self.combatants)
        self.turnManager = turnManager

        self.rollInitiative()

    def rollDice(self, sides) -> int:
        return random.randint(1, sides)

    def rollInitiative(self):
        self.initiativeOrder = {}

        for combatant in self.combatants:
            roll = self.rollDice(20)
            dexMod = combatant.stats.getAbilityMod("DEX")
            initiative = roll + dexMod
            self.initiativeOrder[combatant] = initiative

        sortedCombatants = sorted(self.initiativeOrder.keys(), key= lambda c: self.initiativeOrder[c], reverse=True)

        self.turnQueue = deque(sortedCombatants)

    def displayInitiativeOrder(self):
        print("\n=== Initiative Order ===")
        for index, (combatant, initiative) in enumerate(
            sorted(self.initiativeOrder.items(), key=lambda x: x[1], reverse=True)
        ):
            print(f"{index + 1}. {combatant.name} - Initiative: {initiative}")
        print("==============\n")
    
    def nextTurn(self):
        if self.turnQueue:
            current = self.turnQueue.popleft()
            self.turnQueue.append(current)
            self.turnManager.currentTurnEntity = current
            print(f"Now's {current.name}'s turn. Queue: {[entity.name for entity in self.turnQueue]}")
            self.turnManager.startTurn(current)
        
    def getPlayer(self):
        return self.characters[0] if self.characters else None