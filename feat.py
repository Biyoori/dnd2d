class Feat():
    def __init__(self, name, description, effects):
        self.name = name
        self.description = description
        self.effects = effects

    def apply(self, character):
        for effect in self.effects:
            effect(character)

    def __str__(self):
        return f"{self.name}: {self.description}"