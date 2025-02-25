from typing import Dict, Any

class Race:
    def __init__(self, name: str, raceData: Dict[str, Any]):
        self.name = name
        self.creatureType = raceData["creatureType"]
        print(self.creatureType)
        self.size = raceData["size"]
        print(self.size)
        self.speed = raceData["speed"]
        print(self.speed)
        self.abilityScoreBonuses = raceData["abilityScoreBonuses"]
        print(self.abilityScoreBonuses)
        self.features = raceData["features"]
        print(self.features)

    def applyAbilityBonuses(self, baseStats: dict):
        newStats = baseStats.copy()
        for stat, bonus in self.abilityScoreBonuses.items():
            newStats[stat] += bonus
        print(newStats)
        return newStats

    def __str__(self):
        return f"{self.name} ({self.creatureType}, {self.size}) - Speed: {self.speed}, Traits: {', '.join(self.features)}"