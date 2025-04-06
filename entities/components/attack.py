from random import randint
from typing import TYPE_CHECKING
from ui.game_console import console

if TYPE_CHECKING:
    from entities.entity import Entity

class AttackSystem:
    def resolve_attack(self, attacker: "Entity", target: "Entity") -> None:
        weapon = attacker.weapon_system.get_equipped_weapon()
        attack_roll = randint(1, 20) + attacker.stats.get_attack_bonus(weapon)
        if target.armor_class <= attack_roll:
            damage = attacker.stats.roll_dice(weapon.damage) + attacker.stats.get_damage_bonus(weapon)
            target.health.take_damage(damage, weapon.damage_type)
        else:
            console.log("Attack Missed")
            