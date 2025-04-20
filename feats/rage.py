from core.event import Event
from entities.character.character import Character
from entities.components.health import StatusEffect
from feat import Feat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity



def rage_effect(character: Character) -> None:
    if not Event.notify("use_bonus_action"):
        return
    character.health.add_resistances(["Bludgeoning", "Piercing", "Slashing"])
    if sum(character.levels.get_classes().values()) >= 9:
        rage_bonus = 3
    elif sum(character.levels.get_classes().values()) >= 16:
        rage_bonus = 4
    else:
        rage_bonus = 2
    character.attacking.other_bonuses += rage_bonus
    #Advantage kiedy zrobie do niego system
    #Blokada na spelle

def rage_end(character: "Entity") -> None:
    character.health.remove_resistances(["Bludgeoning", "Piercing", "Slashing"])
    if sum(character.levels.get_classes().values()) >= 9:
        rage_bonus = 3
    elif sum(character.levels.get_classes().values()) >= 16:
        rage_bonus = 4
    else:
        rage_bonus = 2
    character.attacking.other_bonuses -= rage_bonus

rage_status = StatusEffect(name="Rage", duration=10, effect=rage_effect, on_end=rage_end)

def execute_rage(character: "Entity") -> None:
    character.health.set_status(rage_status)

rage = Feat(
    "Rage",
    "...",
    False,
    feat_type="class_specific",
    required_class="Barbarian",
    required_args=["character"],
    on_execute=execute_rage
)
