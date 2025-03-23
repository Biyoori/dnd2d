class SkeletonAi:
    def __init__(self, entity, grid):
        self.entity = entity
        self.grid = grid

    def update(self, target):
        

        meleeAction = next((action for action in self.entity.actions if action["name"] == "Shortsword"), None)

        if meleeAction and self.isInMeleeRange(target, meleeAction["range"]):
            self.entity.executeAction("Shortsword", target)        
        else:
            path = self.grid.calculatePath(self.entity.gridPosition, target.gridPosition)
            nextStep = path[1]
            self.entity.setGridPosition(*nextStep)
            self.entity.setPosition(self.grid)
            print(f"Entity {self.entity.name} moves to ({nextStep[0]}, {nextStep[1]})")

    def isInMeleeRange(self, target, attackRange):
        dx = abs(self.entity.gridPosition[0] - target.gridPosition[0])
        dy = abs(self.entity.gridPosition[1] - target.gridPosition[1])

        return dx <= attackRange//5 and dy <= attackRange