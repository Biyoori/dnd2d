import os
import json
from typing import Dict, Optional
from entities.enemy import Enemy

class EnemyFactory:
    def __init__(self, enemiesDir: str):
        self.enemiesDir = enemiesDir
        self.enemyCache: Dict[str, Dict] = {}

    def loadEnemyData(self, enemyType: str) -> Dict:
        if enemyType in self.enemyCache:
            return self.enemyCache[enemyType]
        
        filepath = os.path.join(self.enemiesDir, f"{enemyType}.json")
        if not os.path.exists(filepath):
            raise ValueError(f"Enemy file not found for: {enemyType}")
        

        with open(filepath, "r") as file:
            data = json.load(file)
            self.enemyCache[enemyType] = data
            return data
        
    def createEnemy(self, enemyType: str) -> "Enemy":
        data = self.loadEnemyData(enemyType)
        return Enemy(**data)