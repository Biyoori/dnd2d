from characters.character import Character
from characters.classes.characterClass import CharacterClass
from characters.race import Race

class CharacterFactory:
    @staticmethod
    def createCharacter(name: str, characterClasses: list[CharacterClass], race: Race, abilityScores: dict[str,int], skillProficiencies: list[str]):
        return Character(
            None, 
            None, 
            None, 
            name, 
            characterClasses, 
            race, 
            abilityScores,
            skillProficiencies
        )