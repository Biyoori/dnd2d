import importlib
from typing import TYPE_CHECKING
from core.event import Event
from entities.components.factions import Faction
from entities.components.health import HealthData, HealthSystem
from entities.components.loot import LootData, LootSystem
from entities.components.stats import AbilityScores, Proficiencies, StatsSystem
from health_calculator import HealthCalculator
from settings import get_color
from ai.skeleton_ai import SkeletonAi
from entities.entity import Entity

if TYPE_CHECKING:
    from core.grid.grid import Grid
    

class Enemy(Entity):
    def __init__(self, grid: "Grid", **kwargs) -> None:
        super().__init__(get_color("blue"), kwargs.get("speed"), Faction.ENEMY)

        self.grid = grid

        self.name = kwargs.get("name", "Unknown")
        self.type = kwargs.get("type", "Unknown")
        self.alignment = kwargs.get("alignment", "Neutral")
        self.armor_class = kwargs.get("armor_class", 10)          
        self.speed = kwargs.get("speed", 30)
        self.condition_immunities = kwargs.get("condition_immunities", [])
        self.senses = kwargs.get("senses", {})
        self.languages = kwargs.get("languages", [])
        self.challenge_rating = kwargs.get("challenge_rating", 0)
        self.experience = kwargs.get("experience", 0)
        self.gear = kwargs.get("gear", [])
        self.actions = kwargs.get("actions", [])
        self.habitat = kwargs.get("habitat", [])    

        #HP
        hit_points = HealthCalculator.calc_enemy(kwargs.get("hit_points", {"fixed": 10}))
        health_data = HealthData(
            hit_points, 
            hit_points, 
            resistances=kwargs.get("damage_resistances", []), 
            immunities=kwargs.get("damage_immunities", []), 
            vulnerabilities=kwargs.get("damage_vulnerabilities", [])
        )
        self.health = HealthSystem(health_data, self)

        #Stats
        abilities = AbilityScores(*kwargs.get("ability_scores", {}).values())
        proficiencies = Proficiencies(kwargs.get("skills", []), [])
        self.stats = StatsSystem(abilities, proficiencies)

        #AI
        self.ai = SkeletonAi(self, self.grid)

        #Loot
        loot_data = LootData({item: 1 for item in kwargs.get("gear", [])})
        self.loot = LootSystem(loot_data)

    def execute_action(self, action_name: str, target: "Entity") -> None:
        action_data = next((action for action in self.actions if action["name"] == action_name), None)
        if not action_data:
            raise ValueError(f"Unknown action: {action_name}")
        
        action_module = action_data.get("code")
        module_name = f"actions.{action_module}"
        try:
            module = importlib.import_module(module_name)
            action_func = getattr(module, "execute")
            action_func(self, target, **action_data)
        except ImportError as e:
            raise ValueError(f"Failed to import action module '{module_name}': {str(e)}")
        except AttributeError as e:
            raise ValueError(f"Module '{module_name}' has no 'execute' function: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error executing action '{action_name}': {str(e)}")
        
    def on_death(self) -> None:
        position = (self.position[0] - self.grid.cell_size // 2, self.position[1] - self.grid.cell_size // 2)
        self.loot.drop_loot(self.position, self.grid_position, self.size)
        Event.notify("enemy_killed", self.experience)
        
        #Remove the enemy from the game
        self.input_handler.entity = None
        self.movement.entity = None
        self.pathfinder.entity = None
        self.ai.entity = None
        self.renderer.entity = None
        Event.notify("remove_enemy", self)


    