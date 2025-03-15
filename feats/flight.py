from feat import Feat

def applyFlight(character):
    character.race.flyingSpeed = max(character.race.flyingSpeed, 50)

flight = Feat(
    name="Flight",
    description="You have a flying speed of 50 feet. To use this speed, you can't be wearing medium or heavy armor.",
    effects=[applyFlight]
)