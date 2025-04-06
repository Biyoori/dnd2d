from optparse import Option
from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity

class Feat():
    def __init__(
        self, 
        name: str, 
        description: str, 
        is_passive: bool, 
        on_apply: Optional[Callable[["Entity"], None]] = None, 
        on_execute: Optional[Callable[..., bool]] = None
    ) -> None:
        
        self.name = name
        self.description = description
        self.is_passive = is_passive
        self.on_apply = on_apply
        self.on_execute = on_execute

    def apply(self, character: "Entity") -> None:
        if self.is_passive and self.on_apply:
            self.on_apply(character)

    def execute(self, character: "Entity", target: Optional["Entity"] = None, **kwargs) -> bool:
        if not self.on_execute:
            return False
        return self.on_execute(character, target, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.description}"