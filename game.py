from entities.components.factions import FactionSystem
from items.weapon import Weapon
from settings import *
from core.grid import Grid
from combat.combat import Combat
from combat.turn_manager import TurnManager
from movement.movement_manager import MovementManager
from factories.enemy_factory import EnemyFactory
from ui.character_creator.character_creator import CharacterCreator
from ui.radial_menu.radial_menu import RadialMenu
from ui.utils import text_renderer
from entity_manager import GameEntityManager

pygame.init()

gameScreen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

text_renderer.init(font_size=40)
faction_system = FactionSystem()
character_creator = CharacterCreator(gameScreen)
enemy_factory = EnemyFactory("data/enemies")
movement_manager = MovementManager()
turn_manager = TurnManager(movement_manager)
entity_manager = GameEntityManager()

grid = Grid()


entity_manager.add_character(character_creator.run())
entity_manager.add_enemy(enemy_factory.create_enemy(grid, "skeleton"))

entity_manager.get_character().inventory.add_item(Weapon("Axe", "", 1, 1, "", "2d4", "Slashing"))
entity_manager.get_character().weapon_system.equip_weapon("Axe")

menu = RadialMenu(entity_manager, grid)
menu.enable_all_sectors(False)
menu.enable_sector("Attack")


print(f"Created: ")
entity_manager.get_character().display_character_info()
print(entity_manager.get_character().race)

gameActive = True


entity_manager.get_enemies()[0].initialize(4,4,grid,movement_manager)
entity_manager.get_character().initialize(1, 1, grid, movement_manager)


combat = Combat([entity_manager.get_character()], [entity_manager.get_enemies()[0]], turn_manager)
turn_manager.start_combat(combat)

def handle_events() -> None:
    global gameActive

    for event in pygame.event.get():
        entity_manager.get_character().update(event, turn_manager)
        menu.process_events(event)  

        if event.type == pygame.QUIT:
            gameActive = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                menu.open_at(event.pos)
            elif event.button == 1:
                 menu.close()
                 if entity_manager.get_character().targeting.target_selection:
                      entity_manager.get_character().targeting.handle_target_selection(event.pos, grid, entity_manager.get_character().attacking, entity_manager.get_character())
            
                      

def draw() -> None:
    gameScreen.fill(get_color("black"))
    grid.draw(gameScreen)
    entity_manager.get_character().draw(gameScreen)
    entity_manager.get_enemies()[0].draw(gameScreen)
    menu.draw(gameScreen)
    pygame.display.flip()

while gameActive:
    handle_events()
    draw()
    clock.tick(framerate)

pygame.quit()



