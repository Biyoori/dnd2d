import random
from collections import deque

class Combat:
    def __init__(self, characters, enemies):
        self.combatants = characters + enemies
        self.turn = 0
        self.initiativeOrder = self.rollInitiative()

    def rollDice(self, sides) -> int:
        return random.randint(1, sides)

    def rollInitiative(self):
        initiativeScores = {}

        for combatant in self.combatants:
            roll = self.rollDice(20)
            dexMod = combatant.stats.getAbilityMod("Dexterity")
            initiative = roll + dexMod
            initiativeScores[combatant] = initiative

            print(f"{combatant.name} rolled {roll} + {dexMod} = {initiative} initiative.")

        sortedCombatants = sorted(initiativeScores.keys(), key=lambda c: initiativeScores[c], reverse=True)

        self.turnQueue = deque(sortedCombatants)

        return initiativeScores
    
    def nextTurn(self):
        if not self.turnQueue:
            print("The initiative queue is empty.")
            return None
        
        self.currentTurn = self.turnQueue.popleft()

        self.turnQueue.append(self.currentTurn)

        print(f"It's {self.currentTurn.name}s turn.")
        return self.currentTurn

    def attack(self, attacker, defender):
        pass