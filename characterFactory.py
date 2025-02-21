import json
from characters.character import Character
from characterClass import CharacterClass

class CharacterFactory:
    @staticmethod
    def createCharacter(name: str, characterClass: CharacterClass):
        return Character(None, None, None, name, characterClass)