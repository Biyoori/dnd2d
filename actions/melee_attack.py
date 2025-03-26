import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.enemy import Enemy
    from entities.entity import Entity

def execute(source: "Enemy", target: "Entity", attack_bonus: int, damage_formula: str, damage_type: str, **kwargs) -> None:
    attack_roll = random.randint(1, 20) + attack_bonus
    if attack_roll >= target.armor_class:
        damage: int = source.stats.roll_dice(damage_formula)
        target.health.take_damage(damage, damage_type)
        print(f"{source.name} uses melee attack dealing {damage} {damage_type} damage!")
    else:
        print(f"{source.name} uses melee attack but misses! {attack_roll}, {target.armor_class}")
