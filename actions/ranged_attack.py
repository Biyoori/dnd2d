import random
from typing import TYPE_CHECKING
from ui.game_console import console

if TYPE_CHECKING:
    from entities.enemy import Enemy
    from entities.entity import Entity

def execute(source: "Enemy", target: "Entity", attack_bonus: int, damage_formula: str, damage_type: str, **kwargs) -> None:
    # Add using ammunition logic here
    name = kwargs.get("name", "Ranged Attack")
    attack_roll = random.randint(1, 20) + attack_bonus
    if attack_roll >= target.armor_class.get_armor_class():
        damage: int = source.stats.roll_dice(damage_formula)
        target.health.take_damage(damage, damage_type)
        console.log(f"{source.name} uses {name} dealing {damage} {damage_type} damage! Roll: {attack_roll} vs AC: {target.armor_class.get_armor_class()}")
    else:
        console.log(f"{source.name} uses {name} but misses! Roll: {attack_roll} vs AC: {target.armor_class.get_armor_class()}")
    # Add logic to check if ammunition is used up or needs to be reloaded here
