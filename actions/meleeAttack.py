import random

def execute(source, target, attack_bonus, damage_formula, damage_type, **kwargs):
    attackRoll = random.randint(1, 20) + attack_bonus
    if attackRoll >= target.armorClass:
        damage = source.stats.rollDice(damage_formula)
        target.takeDamage(damage, damage_type)
        print(f"{source.name} uses melee attack dealing {damage} {damage_type} damage!")
    else:
        print(f"{source.name} uses melee attack but misses! {attackRoll}, {target.armorClass}")
