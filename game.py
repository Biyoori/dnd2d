from core.event import Event
from entities.components.factions import FactionSystem
from items.weapon import Weapon
from settings import *
from core.grid.grid import Grid
from combat.combat import Combat
from combat.turn_manager import TurnManager
from movement.movement_manager import MovementManager
from factories.enemy_factory import EnemyFactory
from ui.inventory_menu import InventoryMenu
from ui.feat_menu_manager import FeatMenuManager
from ui.character_creator.character_creator import CharacterCreator
from ui.game_console import console
from ui.level_up_menu import ClassSelectionUI
from ui.main_menu import MainMenu
from ui.radial_menu.radial_menu import RadialMenu
from ui.turn_ui import TurnInfo
from ui.utils import text_renderer
from entity_manager import GameEntityManager

pygame.init()

gameScreen = pygame.display.set_mode((screen_width, screen_height))
game_layer = pygame.Surface((screen_width, screen_height))
character_layer = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("Assets/UI/Fonts/IM_Fell_DW_Pica/IMFellDWPica-Regular.ttf", 24)

text_renderer.init(font_size=40)
main_menu = MainMenu(gameScreen)
faction_system = FactionSystem()
character_creator = CharacterCreator(gameScreen)
enemy_factory = EnemyFactory("data/enemies")
movement_manager = MovementManager()
turn_manager = TurnManager(movement_manager)
entity_manager = GameEntityManager()
turn_info = TurnInfo(turn_manager, gameScreen)
feat_menu_manager = FeatMenuManager(gameScreen)
level_up_ui = ClassSelectionUI(gameScreen, font)
inventory_menu = InventoryMenu(font, gameScreen)

grid = Grid()
grid.generator.generate_bsp(20, 5)

main_menu.display_menu()


entity_manager.add_character(character_creator.run())
entity_manager.add_enemy(enemy_factory.create_enemy(grid, "skeleton"))

grid.generator.spawn_entities(entity_manager.get_character(), entity_manager.get_enemies())

menu = RadialMenu(entity_manager, grid, feat_menu_manager)
menu.enable_all_sectors(False)
menu.enable_sector("Attack")
menu.enable_sector("Abilities")
menu.enable_sector("Items")


print(f"Created: ")
entity_manager.get_character().display_character_info()
print(entity_manager.get_character().race)

gameActive = True


entity_manager.get_enemies()[0].initialize(*entity_manager.get_enemies()[0].grid_position, grid,movement_manager)
entity_manager.get_character().initialize(*entity_manager.get_character().grid_position, grid, movement_manager)

combat = Combat([entity_manager.get_character()], entity_manager.get_enemies(), turn_manager)
turn_manager.start_combat(combat)
print(Event.list_events())


def handle_events() -> None:
    global gameActive

    for event in pygame.event.get():
        entity_manager.get_character().update(event, turn_manager)
        menu.process_events(event)
        level_up_ui.handle_event(event)
        inventory_menu.handle_event(event)
        
        if event.type == pygame.QUIT:
            gameActive = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and not entity_manager.get_character().input_handler.dragging:
                menu.open_at(event.pos)
            elif event.button == 1:
                menu.close()
                if entity_manager.get_character().targeting.target_selection:
                    entity_manager.get_character().targeting.handle_target_selection(event.pos, grid, entity_manager.get_character().attacking, entity_manager.get_character(), turn_manager)
        if event.type == pygame.MOUSEWHEEL:
            grid.cell_size += event.y
            entity_manager.get_character().update_size(grid)
            entity_manager.get_character().movement.set_position(*entity_manager.get_character().grid_position)
            for enemy in entity_manager.get_enemies():
                enemy.update_size(grid)
                enemy.movement.set_position(*enemy.grid_position)
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            turn_manager.end_turn()
            

def draw() -> None:
    gameScreen.fill(get_color("black"))
    grid.renderer.render(gameScreen)
    
    entity_manager.get_character().draw(gameScreen)
    entity_manager.get_enemies()[0].draw(gameScreen)

    entity_manager.get_character().pathfinder.draw_path(gameScreen, grid.cell_size)

    menu.draw(gameScreen)
    turn_info.draw()
    level_up_ui.draw()
    console.draw(gameScreen)
    inventory_menu.draw_menu()
    pygame.display.flip()

def update_enemies() -> None:
    for enemy in entity_manager.get_enemies():
        if enemy.health.is_alive():
            pass
        else:
            pass
            #enemy.die()
            #entity_manager.remove_enemy(enemy)
            #combat.remove_enemy(enemy)

while gameActive:
    draw()
    handle_events()
    update_enemies()
    clock.tick(framerate)

pygame.quit()



