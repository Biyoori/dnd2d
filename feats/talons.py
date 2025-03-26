from feat import Feat

def apply_talons(character) -> None:
    pass

talons = Feat(
    name="Talons",
    description="Your talons are natural weapons, which you can use to make unarmed strikes. If you hit with them, you deal slashing damage equal to 1d4 + your Strength modifier, instead of the bludgeoning damage normal for an unarmed strike.",
    effects=[apply_talons]
)