class MovementManager:
    def __init__(self):
        self.movementUsed = {}

    def resetMovement(self, entity):
        self.movementUsed[entity] = 0

    def canMove(self, entity, tiles):
        maxTiles = entity.maxTiles
        return self.movementUsed.get(entity, 0) + tiles<= maxTiles
    
    def registerMovement(self, entity, tiles, turnManager):
        if turnManager.isInCombat():
            if entity in self.movementUsed:
                self.movementUsed[entity] += tiles
            else:
                self.movementUsed[entity] = tiles

            if self.movementUsed[entity] >= entity.maxTiles and turnManager.isInCombat():
                turnManager.endCombat()

    def resetAllMovement(self):
        self.movementUsed.clear()
        print(f"movement cleared: {self.movementUsed}")