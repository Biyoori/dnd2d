from typing import Callable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity

class Feat():
    def __init__(
        self, 
        name: str, 
        description: str, 
        is_passive: bool,
        required_args: Optional[List[str]] = None, 
        on_apply: Optional[Callable[["Entity"], None]] = None, 
        on_execute: Optional[Callable[..., bool]] = None,
    ) -> None:
        
        self.name = name
        self.description = description
        self.is_passive = is_passive
        self.required_args = required_args
        self.on_apply = on_apply
        self.on_execute = on_execute

    def apply(self, character: "Entity") -> None:
        if self.is_passive and self.on_apply:
            self.on_apply(character)

    def execute(self, **kwargs) -> bool:
        if not self.on_execute:
            return False
        
        missing = [arg for arg in self.required_args if arg not in kwargs]
        if missing:
            raise ValueError(f"missing required args: {missing}")
        
        return self.on_execute(**kwargs)

    def __str__(self):
        return f"{self.name}: {self.description}"