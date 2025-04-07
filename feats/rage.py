from feat import Feat

def execute_rage():
    pass

rage = Feat(
    "Rage",
    "...",
    False,
    feat_type="class_specific",
    required_class="Barbarian",
    on_execute=execute_rage
)
