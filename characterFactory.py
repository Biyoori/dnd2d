import json
from characters.character import Character
from characterClass import CharacterClass
from race import Race

class CharacterFactory:
    @staticmethod
    def createCharacter(name: str, characterClass: CharacterClass, race: Race):
        return Character(
            None, 
            None, 
            None, 
            name, 
            characterClass, 
            race, 
            {
            "Strength": 10,
            "Dexterity": 10,
            "Constitution": 10,
            "Intelligence": 10,
            "Wisdom": 10,
            "Charisma": 10
            }

        )