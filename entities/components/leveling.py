from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Dict, List
from core.event import Event

if TYPE_CHECKING:
    from characters.classes.characterClass import CharacterClass

@dataclass
class LevelingData:
    primary_class: "CharacterClass"
    experience: int
    character_classes: Dict["CharacterClass", int] = field(default_factory=dict)
    XP_TRESHOLDS: ClassVar[List[int]] = [0, 300, 900, 2700, 6500, 14000, 34000, 48000, 64000]

class LevelingSystem:
    def __init__(self, leveling_data: LevelingData) -> None:
        self._levels = leveling_data
        self.selected_class = None
        
        Event.subscribe("class_selected", self._set_selected_class)

    def add_exp(self, amount) -> None:
        self._levels.experience += amount
        if sum(self._levels.character_classes.values()) < len(self._levels.XP_TRESHOLDS) and self._levels.experience >= self._levels.XP_TRESHOLDS[sum(self._levels.character_classes.values())]:
            Event.notify("show_class_selection_ui")

    def level_up(self, character_class: "CharacterClass") -> None:
        if character_class in self._levels.character_classes:
            self._levels.character_classes[character_class] += 1
        else:
            self._levels.character_classes[character_class] = 1

        new_feats = next(
            char_class for char_class in self._levels.character_classes if char_class == character_class
        ).get_feats_for_level(self._levels.character_classes[character_class])

        level_sum = sum(level for level in self._levels.character_classes.values())
        Event.notify("level_up", level_sum, character_class, new_feats)
    
    def _set_selected_class(self, selected_class: "CharacterClass") -> None:
        self.selected_class = selected_class
        self.level_up(self.selected_class)

    def get_classes(self) -> Dict["CharacterClass", int]:
        return self._levels.character_classes.copy()
    
    def get_primary_class(self) -> "CharacterClass":
        return self._levels.primary_class