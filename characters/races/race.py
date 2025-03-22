from typing import Dict, Any

class Race:
    def __init__(self, name: str, raceData: Dict[str, Any]):
        self.name = name
        self.creatureType = raceData["creatureType"]
        self.size = raceData["size"]
        self.walkingSpeed = raceData["speed"]
        self.flyingSpeed = 0
        self.abilityScoreBonuses = raceData["abilityScoreBonuses"]
        self.features = raceData["features"]

    def applyAbilityBonuses(self, baseStats: dict):
        newStats = baseStats.copy()
        for stat, bonus in self.abilityScoreBonuses.items():
            newStats[stat] += bonus
        return newStats

    def __str__(self):
        return f"{self.name} ({self.creatureType}, {self.size}) - Speed: {self.walkingSpeed}, Flying Speed: {self.flyingSpeed}, Traits: {', '.join(self.features)}"