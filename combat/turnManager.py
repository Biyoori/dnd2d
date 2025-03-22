class TurnManager:
    def __init__(self, movementManager):
        self.inCombat = False
        self.currentTurnEntity = None
        self.movementManager = movementManager

    def startCombat(self, combat):
        self.combat = combat
        self.inCombat = True
        combat.displayInitiativeOrder()
        self.currentTurnEntity = combat.nextTurn()

    def endCombat(self):
        self.inCombat = False
        self.currentTurnEntity = None
        self.movementManager.resetAllMovement()
        print(f"combat end")

    def startTurn(self, entity):
        self.currentTurnEntity = entity
        self.movementManager.resetMovement(entity)
        print(entity.name)

    def nextTurn(self):
        if self.inCombat:
            self.currentTurnEntity = self.combat.nextTurn()

    def endTurn(self):
        print(f"{self.currentTurnEntity.name} finished their turn!")
        self.nextTurn()

    def isCurrentTurn(self, entity):
        if not self.inCombat:
            return True
        return self.currentTurnEntity is entity
    
    def isInCombat(self):
        return self.inCombat