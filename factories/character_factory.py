from tracemalloc import start
from entities.character.character import Character
from characters.classes.characterClass import CharacterClass
from characters.races.race import Race

class CharacterFactory:
    @staticmethod
    def create_character(name: str, character_classes: list[CharacterClass], race: Race, ability_scores: dict[str,int], skill_proficiencies: list[str], starting_gear: list[list[str]]) -> Character:
        return Character(
            name, 
            character_classes, 
            race, 
            ability_scores,
            skill_proficiencies,
            starting_gear
        )