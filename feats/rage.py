from feat import Feat

class Rage(Feat):
    pass

def execute_rage(self) -> None:
    if 

rage = Feat(
    "Rage",
    "...",
    False,
    feat_type="class_specific",
    required_class="Barbarian",
    on_execute=execute_rage
)
