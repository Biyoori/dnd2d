from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.components.stats import StatsSystem
    from entities.components.feats import FeatSystem
    from entities.components.armors import ArmorSystem

class ArmorClass:
    def __init__(self) -> None:
        self._armor_class = 10
        self._source = ""

    def calculate_ac(self, armors: "ArmorSystem", stats: "StatsSystem", feats: "FeatSystem") -> int:
        dex = stats.get_mod("DEX")
        con = stats.get_mod("CON")
        
        wearing_armor = armors.get_equipped_armor()
        if wearing_armor:
            self._armor_class = wearing_armor.armor_class + dex
            self._source = "Armor"
        elif not wearing_armor and feats.has_feat("Unarmored Defense"):
            self._armor_class = 10 + dex + con
            self._source = "Unarmored Defense"
        else:
            self._armor_class = 10 + dex
            self._source = "Unarmored"
        return self._armor_class
    
    def get_armor_class(self) -> int:
        return self._armor_class