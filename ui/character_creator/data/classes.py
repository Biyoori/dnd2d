from characters.classes import Barbarian, Fighter
from characters.classes.characterClass import CharacterClass

CHARACTER_CLASSES = [Barbarian(), Fighter()]

def get_classes() -> list[CharacterClass]:
    return CHARACTER_CLASSES