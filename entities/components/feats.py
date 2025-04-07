from dataclasses import dataclass, field
from typing import Dict, List, TYPE_CHECKING, Optional
from feat import Feat
from core.feat_loader import get_feat

if TYPE_CHECKING:
    from entities.entity import Entity
    from characters.classes.characterClass import CharacterClass

@dataclass
class FeatsData:
    available_feats: Dict[str, "Feat"] = field(default_factory=dict)
    active_feats: List[str] = field(default_factory=set)
    passive_feats: List[str] = field(default_factory=set)

class FeatSystem:
    def __init__(self, owner: "Entity", feats: FeatsData) -> None:
        self.owner = owner
        self._feats = feats

    def add_feat(self, feat: "Feat"):
        self._feats.available_feats[feat.name] = feat

        if feat.is_passive:
            self._feats.passive_feats.add(feat.name)
            feat.apply(self.owner)
        else:
            self._feats.active_feats.add(feat.name)

    def execute(self, feat_name: str, target: Optional["Entity"] = None, **kwargs):
        if feat_name not in self._feats.active_feats:
            return False
        
        if feat := self._feats.available_feats.get(feat_name):
            return feat.execute(self.owner, target, **kwargs)
        
        return False
    
    def get_feats(self) -> Dict[str, Feat]:
        return self._feats.available_feats.copy()
    
    def get_active(self) -> List[str]:
        return self._feats.active_feats.copy()
    
    def add_feats_on_level_up(self, level: int, character_class: "CharacterClass", feats: List[str]) -> None:
        for feat in feats:
            self.add_feat(get_feat(feat))