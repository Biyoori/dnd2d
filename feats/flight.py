from feat import Feat

def apply_flight(character) -> None:
    character.race.flying_speed = max(character.race.flying_speed, 50)

flight = Feat(
    name="Flight",
    description="You have a flying speed of 50 feet. To use this speed, you can't be wearing medium or heavy armor.",
    effects=[apply_flight]
)