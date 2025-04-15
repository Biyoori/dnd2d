from core.event import Event
from core.feat_loader import get_feat
from entities.components.armor_class import ArmorClass
from entities.components.armors import ArmorSystem
from entities.components.attack import AttackSystem
from entities.components.factions import Faction, FactionSystem
from entities.components.feats import FeatSystem, FeatsData
from entities.components.health import HealthData, HealthSystem
from entities.components.inventory import InventoryData, InventorySystem
from entities.components.leveling import LevelingData, LevelingSystem
from entities.components.stats import AbilityScores, Proficiencies, StatsSystem
from entities.components.target import TargetingSystem
from entities.components.weapons import WeaponSystem
from items.armor import Armor
from settings import get_color
from entities.entity import Entity
from health_calculator import HealthCalculator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...characters.classes.characterClass import CharacterClass
    from ...characters.races.race import Race
    from items.item import Item

class Character(Entity):
    def __init__(
            self,
            name: str, 
            character_classes: "CharacterClass", 
            race: "Race", 
            ability_scores: dict[str,int],
            skill_proficiencies: list[str]
        ) -> None: 
        super().__init__(get_color("red"), race.walking_speed, Faction.PLAYER)
        self.name = name

        self.race = race

        # Character Classes and Leveling
        level_data = LevelingData(character_classes, 0, {character_classes: 1})
        self.levels = LevelingSystem(level_data)

        # Stats
        abilities = AbilityScores(*[score for score in ability_scores.values()])
        proficiencies = Proficiencies(skill_proficiencies, self.levels.get_primary_class().saving_throws)
        self.stats = StatsSystem(abilities, proficiencies, self.get_proficiency_bonus())

        #Inventory
        inventory_data = InventoryData([])
        self.inventory = InventorySystem(inventory_data)

        #Weapon System
        self.weapon_system = WeaponSystem(self.inventory)

        # Armor System
        self.armor_system = ArmorSystem(self.inventory)

        #Attacking and Targeting
        factions = FactionSystem()
        self.targeting = TargetingSystem(factions)
        self.attacking = AttackSystem()
        
        # Hit Points
        hp = HealthCalculator.calc_character(self.levels.get_classes(), self.stats)
        health_data = HealthData(hp, hp)
        self.health = HealthSystem(health_data, self)

        # Feats
        self.feats = FeatSystem(self, FeatsData())
        for feat in self.load_feats():
            self.feats.add_feat(feat)
        for feat in self.levels.get_primary_class().feats_by_level[1]:
            self.feats.add_feat(get_feat(feat))

        # Armor Class
        self.armor_class = ArmorClass()
        self.armor_class.calculate_ac(self.armor_system, self.stats, self.feats)

        #Level up subscribtions
        Event.subscribe("level_up", self.health.increase_health_on_level_up)
        Event.subscribe("level_up", self.feats.add_feats_on_level_up)
        Event.subscribe("level_up", self.stats.stats_increase_on_level_up)
    
    def get_proficiency_bonus(self) -> int:
        level = sum(lvl for lvl in self.levels.get_classes().values())
        return 2 + (level - 1) // 4
    
    def load_feats(self) -> list:
        return [get_feat(feat) for feat in self.race.features]

    def pick_up(self, item: "Item") -> None:
        self.inventory.add_item(item)

    def drop(self, item_name: str) -> None:
        self.inventory.remove_item(item_name)

    def display_character_info(self) -> None:
        print(f"{self.name}, {self.race.name}")
        print("Classes:", {cls.name: lvl for cls, lvl in self.levels.get_classes().items()})
        print("Skills:", self.stats._proficiencies.skills)