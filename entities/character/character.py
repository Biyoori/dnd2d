from core.feat_loader import get_feat
from entities.components.attack import AttackSystem
from entities.components.factions import Faction, FactionSystem
from entities.components.health import HealthData, HealthSystem
from entities.components.inventory import InventoryData, InventorySystem
from entities.components.stats import AbilityScores, Proficiencies, StatsSystem
from entities.components.target import TargetingSystem
from entities.components.weapons import WeaponSystem
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
        self.experience = 0      
        self.armor_class = 10
        self.race = race

        # Character Classes
        self.primary_class = character_classes
        self.character_classes = {character_classes: 1}

        # Stats
        abilities = AbilityScores(*[score for score in ability_scores.values()])
        proficiencies = Proficiencies(skill_proficiencies, self.primary_class.saving_throws)
        self.stats = StatsSystem(abilities, proficiencies, self.get_proficiency_bonus())

        #Inventory
        inventory_data = InventoryData([])
        self.inventory = InventorySystem(inventory_data)

        #Weapon System
        self.weapon_system = WeaponSystem(self.inventory)

        #Attacking and Targeting
        factions = FactionSystem()
        self.targeting = TargetingSystem(factions)
        self.attacking = AttackSystem()
        
        # Hit Points
        hp = HealthCalculator.calc_character(self.character_classes, self.stats)
        health_data = HealthData(hp, hp)
        self.health = HealthSystem(health_data, self)

        # Feats
        self.feats =  self.load_feats()
        self.apply_feats()
    
    def get_proficiency_bonus(self) -> int:
        level = sum(lvl for lvl in self.character_classes.values())
        return 2 + (level - 1) // 4
    
    def load_feats(self) -> list:
        return [get_feat(feat) for feat in self.race.features]
    
    def apply_feats(self) -> None:
        for feat in self.feats:
            feat.apply(self)

    def pick_up(self, item: "Item") -> None:
        self.inventory.add_item(item)

    def drop(self, item_name: str) -> None:
        self.inventory.remove_item(item_name)

    def display_character_info(self) -> None:
        print(f"{self.name}, {self.race.name}")
        print("Classes:", {cls.name: lvl for cls, lvl in self.character_classes.items()})
        print("Skills:", self.stats._proficiencies.skills)