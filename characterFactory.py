from characters.character import Character
from characterClass import CharacterClass
from race import Race

class CharacterFactory:
    @staticmethod
    def createCharacter(name: str, characterClass: CharacterClass, race: Race, abilityScores: dict[str,int]):
        return Character(
            None, 
            None, 
            None, 
            name, 
            characterClass, 
            race, 
            abilityScores

        )