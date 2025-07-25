from dataclasses import dataclass
from feat import Feat
from items.weapon import Weapon
from typing import TYPE_CHECKING, ClassVar, List
from debugging import logger

if TYPE_CHECKING:
    from entities.entity import Entity
    from core.grid.grid import Grid

@dataclass
class TalonsWeapon(Weapon):
    def __init__(self) -> None:
        super().__init__(
            name="Talons",
            description="Natural weapons dealing slashing damage", 
            weight=0, 
            value=0, 
            weapon_type="Unarmed", 
            damage="1d6", 
            damage_type="Slashing",
            properties=["Natural"],
        )

class TalonsFeat(Feat):
    _talons_weapon: ClassVar[Weapon] = TalonsWeapon()

    def __init__(self) -> None:
        super().__init__(
            name="Talons", 
            description="Your talons are natural weapons...", 
            is_passive=False,
            feat_type="racial",
            required_args=["character", "grid", "entities"],
            on_execute=self.execute_talons
        )

    @classmethod
    def execute_talons(cls, character: "Entity", grid: "Grid", entities: List["Entity"], **__) -> bool:
        if not entities:
            return False

        current_weapon = None
        try:
            current_weapon = character.weapon_system.get_equipped_weapon()
            character.weapon_system.equip_weapon_directly(cls._talons_weapon)
            character.targeting.get_valid_targets(character, entities, grid)

            return True

        except Exception as e:
            logger.log(f"Error executing Talons: {e}", "ERROR")
            return False
        finally:
            if current_weapon:
                character.weapon_system.equip_weapon_directly(current_weapon)

talons = TalonsFeat()