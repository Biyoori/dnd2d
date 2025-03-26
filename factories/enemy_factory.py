import os
import json
from typing import TYPE_CHECKING, Dict
from entities.enemy import Enemy

if TYPE_CHECKING:
    from tkinter import Grid

class EnemyFactory:
    def __init__(self, enemies_dir: str) -> None:
        self.enemies_dir = enemies_dir
        self.enemy_cache: Dict[str, Dict] = {}

    def load_enemy_data(self, enemy_type: str) -> Dict[str, Dict]:
        if enemy_type in self.enemy_cache:
            return self.enemy_cache[enemy_type]
        
        filepath = os.path.join(self.enemies_dir, f"{enemy_type}.json")
        if not os.path.exists(filepath):
            raise ValueError(f"Enemy file not found for: {enemy_type}")
        

        with open(filepath, "r") as file:
            data = json.load(file)
            self.enemy_cache[enemy_type] = data
            return data
        
    def create_enemy(self, grid: "Grid", enemy_type: str) -> "Enemy":
        data = self.load_enemy_data(enemy_type)
        return Enemy(grid, **data)