import importlib
from settings import getColorFromPallette
from entities.entity import Entity
from core.statsManager import StatsManager


class Enemy(Entity):
    def __init__(self, **kwargs):
        print(kwargs.get("speed"))
        super().__init__(getColorFromPallette("blue"), kwargs.get("speed"))

        self.name = kwargs.get("name", "Unknown")
        self.type = kwargs.get("type", "Unknown")
        self.alignment = kwargs.get("alignment", "Neutral")
        self.armorClass = kwargs.get("armor_class", 10)
        self.hitPointsData = kwargs.get("hit_points", {"fixed": 10})
        self.hitPoints = self.calculateHitPoints()
        self.speed = kwargs.get("speed", 30)
        self.skills = kwargs.get("skills", {})
        self.damageResistances = kwargs.get("damage_resistances", [])
        self.damageImmunities = kwargs.get("damage_immunities", [])
        self.conditionImmunities = kwargs.get("condition_immunities", [])
        self.damageVulnerabilities = kwargs.get("damage_vulnerabilities", [])
        self.senses = kwargs.get("senses", {})
        self.languages = kwargs.get("languages", [])
        self.challengeRating = kwargs.get("challenge_rating", 0)
        self.experience = kwargs.get("experience", 0)
        self.gear = kwargs.get("gear", [])
        self.actions = kwargs.get("actions", [])
        self.habitat = kwargs.get("habitat", [])
        
        self.stats = StatsManager(kwargs.get("ability_scores", {}))

    def calculateHitPoints(self) -> int:
        if "fixed" in self.hitPointsData:
            return self.hitPointsData["fixed"]
        elif "formula" in self.hitPointsData:
            #return rollowanie na hp
            pass
        else:
            raise ValueError("No 'formula' or 'fixed' in hit point data")

    def executeAction(self, actionName: str, target: "Entity") -> None:
        actionData = next((action for action in self.actions if action["name"] == actionName), None)

        if not actionData:
            raise ValueError(f"Unknown action: {actionName}")
        
        actionModule = actionData.get("code")
        moduleName = f"actions.{actionModule}"
        try:
            module = importlib.import_module(moduleName)
            actionFunc = getattr(module, "execute")
            actionFunc(self, target, **actionData)
        except (ImportError, AttributeError):
            raise ValueError(f"Cant load the action: {actionModule}")

    