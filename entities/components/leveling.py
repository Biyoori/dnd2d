from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List
from characters.classes.barbarian import Barbarian
from characters.classes.characterClass import CharacterClass
from core.event import Event

if TYPE_CHECKING:
    from characters.classes.characterClass import CharacterClass

@dataclass
class LevelingData:
    primary_class: "CharacterClass"
    experience: int
    character_classes: Dict["CharacterClass", int] = field(default_factory=dict)
    experience_to_next_level: int = 100

class LevelingSystem:
    def __init__(self, leveling_data: LevelingData) -> None:
        self._levels = leveling_data
        self.on_level_up = Event()

    def add_exp(self, amount) -> None:
        self._levels.experience =+ amount
        while self._levels.experience >= self._levels.experience_to_next_level:
            self._levels.experience_to_next_level = 300
            self.level_up(Barbarian())

    def level_up(self, character_class: "CharacterClass") -> None:
        if character_class in self._levels.character_classes:
            self._levels.character_classes[character_class] += 1
        else:
            self._levels.character_classes[character_class] = 1

        new_feats = next(
            char_class for char_class in self._levels.character_classes if char_class == character_class
        ).get_feats_for_level(self._levels.character_classes[character_class])
        level_sum = sum(level for level in self._levels.character_classes.values())
        self.on_level_up.notify(level_sum, character_class, new_feats)

    def get_classes(self) -> Dict[CharacterClass, int]:
        return self._levels.character_classes.copy()
    
    def get_primary_class(self) -> CharacterClass:
        return self._levels.primary_class