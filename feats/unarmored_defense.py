
from feat import Feat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity

def apply_unarmored_defense(character: "Entity"):
    pass

unarmored_defense = Feat(
    "Unarmored Defense",
    "...",
    True,
    feat_type="class_specific",
    required_class="Barbarian",
    on_apply=apply_unarmored_defense
)