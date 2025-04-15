from math import ceil
from typing import Set, List, TYPE_CHECKING
from dataclasses import dataclass, field
from ui.game_console import console

if TYPE_CHECKING:
    from entities.entity import Entity
    from characters.classes.characterClass import CharacterClass

@dataclass(frozen=True)
class HealthData:
    max_hp: int
    current_hp: int
    is_alive: bool = True
    resistances: Set[str] = field(default_factory=set)
    immunities: Set[str] = field(default_factory=set)
    vulnerabilities: Set[str] = field(default_factory=set)

    @classmethod
    def create(cls, base_hp: int, con_mod: int, **kwargs) -> "HealthData":
        return cls(
            max_hp=base_hp + con_mod,
            current_hp=base_hp + con_mod,
            is_alive=True,
            resistances=kwargs.get("resistances", set()),
            immunities=kwargs.get("immunities", set()),
            vulnerabilities=kwargs.get("vulnerabilities", set()) 
        )
    
@dataclass
class StatusEffect:
    name: str
    duration: int
    effect: callable
    on_end: callable

class HealthSystem:
    def __init__(self, health_data: HealthData, entity: "Entity") -> None:
        self._data = health_data
        self._entity = entity
        self._status_effects: List[StatusEffect] = []

    def take_damage(self, damage, damage_type) -> HealthData: 

        new_hp = max(0, self._data.current_hp - damage)
        self._data = HealthData(
            max_hp=self._data.max_hp,
            current_hp=new_hp,
            is_alive=new_hp>0,
            resistances=self._data.resistances,
            immunities=self._data.immunities,
            vulnerabilities=self._data.vulnerabilities
        )
        console.log(f"{self._entity.name} takes {damage} {damage_type} damage! Current health: {self._data.current_hp}")
        return self._data
    
    def heal(self, amount: int) -> HealthData:
        
        new_hp = min(self._data.max_hp, self._data.current_hp + amount)
        self._data = HealthData(
            max_hp=self._data.max_hp,
            current_hp=new_hp,
            is_alive=new_hp>0,
            resistances=self._data.resistances,
            immunities=self._data.immunities,
            vulnerabilities=self._data.vulnerabilities
        )
        console.log(f"{self._entity.name} is healed for {amount} hit points! Current health: {self._data.current_hp}")
        return self._data
    
    def add_resistances(self, resistances: List[str]) -> HealthData:
        current_resistances = self._data.resistances 
        print(self._data.resistances)
        for resistance in resistances:
            current_resistances.add(resistance)
        self._data = HealthData(
            max_hp=self._data.max_hp,
            current_hp=self._data.current_hp,
            is_alive=self._data.is_alive,
            resistances=current_resistances,
            immunities=self._data.immunities,
            vulnerabilities=self._data.vulnerabilities
        )
        return self._data
    
    def remove_resistances(self, resistances: List[str]):
        current_resistances = self._data.resistances
        for resistance in resistances:
            try:
                current_resistances.remove(resistance)
            except:
                print(f"Reistance - {resistance} not found.")
        self._data = HealthData(
            max_hp=self._data.max_hp,
            current_hp=self._data.current_hp,
            is_alive=self._data.is_alive,
            resistances=current_resistances,
            immunities=self._data.immunities,
            vulnerabilities=self._data.vulnerabilities
        )
        return self._data
    
    def get_resistances(self) -> Set[str]:
        return self._data.resistances.copy()
    
    def set_status(self, status: StatusEffect) -> None:
        self._status_effects.append(status)
        status.effect(self._entity)

    def remove_status(self, status_name: str) -> None:
        self._status_effect = [status for status in self._status_effects if status.name != status_name]

    def status_update(self) -> None:
        for status in self._status_effects[:]:
            status.duration -= 1
            if status.duration <= 0:
                if status.on_end:
                    status.on_end(self._entity)
                self._status_effects.remove(status)

    def increase_health_on_level_up(self, level: int, character_class: "CharacterClass", feats: List[str]) -> HealthData:
        new_max_hp: int = ceil(character_class.hit_die/2) + self._entity.stats.get_mod("CON")

        self._data = HealthData(
            max_hp=new_max_hp,
            current_hp=min(self._data.current_hp + new_max_hp, new_max_hp),
            is_alive=self._data.current_hp>0,
            resistances=self._data.resistances,
            immunities=self._data.immunities,
            vulnerabilities=self._data.vulnerabilities
        )
        return self._data