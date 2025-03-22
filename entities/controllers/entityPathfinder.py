class EntityPathfinder:
    def __init__(self, grid: "Grid"): #type: ignore
        self.grid = grid
        self._tempPath = []
        self.pathStartX, self.pathStartY = 0, 0

    @property
    def tempPath(self) -> list[tuple[int, int]]:
        return self._tempPath.copy()

    def startMovement(self, pathStartX: int, pathStartY: int) -> None:
        self.pathStartX, self.pathStartY = pathStartX, pathStartY
        self.grid.navigationPath = [(pathStartX, pathStartY)]
        self._tempPath = []

    def updatePath(self) -> None:
        if len(self.grid.navigationPath) > 1:
            self._tempPath = self.grid.navigationPath[:-1]
            self.pathStartX, self.pathStartY = self.grid.navigationPath[-1]

    def calculatePath(self, newX: int, newY: int) -> list[tuple[int, int]]:
        return self.grid.calculatePath((self.pathStartX, self.pathStartY), (newX, newY))
    
    def clearPath(self):
        self._tempPath = []
        self.grid.navigationPath = []