from settings import *
from core.grid import Grid
from combat.combat import Combat
from combat.turn_manager import TurnManager
from movement.movement_manager import MovementManager
from factories.enemy_factory import EnemyFactory
from ai.skeleton_ai import SkeletonAi
from ui.character_creator.character_creator import CharacterCreator
from ui.radial_menu.components.sector_factory import SectorFactory
from ui.radial_menu.radial_menu import RadialMenu
from ui.utils.text_renderer import init

pygame.init()

gameScreen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

init(font_size=40)
character_creator = CharacterCreator(gameScreen)
enemy_factory = EnemyFactory("data/enemies")
movement_manager = MovementManager()
turn_manager = TurnManager(movement_manager)

grid = Grid()

menu = RadialMenu(6)

testCharacter = character_creator.run()
skeleton = enemy_factory.create_enemy(grid, "skeleton")

print(f"Created: ")
testCharacter.display_character_info()
print(testCharacter.race)

gameActive = True


skeleton.initialize(4,4,grid,movement_manager)
testCharacter.initialize(1, 1, grid, movement_manager)
testCharacter.health.take_damage(5, "Fire")


combat = Combat([testCharacter], [skeleton], turn_manager)
turn_manager.start_combat(combat)

def handle_events() -> None:
    global gameActive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 3:
                menu.open_at(event.pos)
            elif event.button == 1:
                menu.close()
                
        testCharacter.update(event, turn_manager)
        menu.process_events(event)

def draw() -> None:
    gameScreen.fill(get_color_from_pallette("black"))
    grid.draw(gameScreen)
    testCharacter.draw(gameScreen)
    skeleton.draw(gameScreen)
    menu.draw(gameScreen)
    pygame.display.flip()

while gameActive:
    handle_events()
    draw()
    clock.tick(framerate)

pygame.quit()



