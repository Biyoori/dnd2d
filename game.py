from doctest import debug
from math import pi
from core.camera import Camera
from debugging import logger, DebugOverlay, DebugConsole
from entities import entity
from entities.components.factions import FactionSystem
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

entity_manager = GameEntityManager()
log_overlay = DebugOverlay(pygame.font.Font(None, 18))
debug_console = DebugConsole(entity_manager)
text_renderer.init(font_size=40)
main_menu = MainMenu(gameScreen)
faction_system = FactionSystem()
character_creator = CharacterCreator(gameScreen)
enemy_factory = EnemyFactory("data/enemies")
movement_manager = MovementManager()
camera = Camera()

turn_manager = TurnManager(movement_manager)
turn_info = TurnInfo(turn_manager, gameScreen)
feat_menu_manager = FeatMenuManager(gameScreen)
level_up_ui = ClassSelectionUI(gameScreen, font)
inventory_menu = InventoryMenu(font, gameScreen)

grid = Grid()
rooms = grid.generator.generate_rp(10)

main_menu.display_menu()


entity_manager.add_character(character_creator.run())
for enemy in range(1):
    entity_manager.add_enemy(enemy_factory.create_enemy(grid, "skeleton"))
    

grid.generator.spawn_entities(entity_manager.get_character(), entity_manager.get_enemies(), rooms)

menu = RadialMenu(entity_manager, grid, feat_menu_manager)
menu.enable_all_sectors(False)
menu.enable_sector("Attack")
menu.enable_sector("Abilities")
menu.enable_sector("Items")


print(f"Created: ")
entity_manager.get_character().display_character_info()
print(entity_manager.get_character().race)

gameActive = True

for enemy in entity_manager.get_enemies():
    if enemy.grid_position == (0, 0):
        entity_manager.remove_enemy(enemy)
        del enemy
    enemy.initialize(*enemy.grid_position, grid, movement_manager)
entity_manager.get_character().initialize(*entity_manager.get_character().grid_position, grid, movement_manager)

combat = Combat([entity_manager.get_character()], [], turn_manager)

def handle_events() -> None:
    global gameActive

    for event in pygame.event.get():
        if entity_manager.get_character().health.is_alive():
            if hasattr(event, 'pos'):
                mouse_pos, _ = camera.apply_offset(event.pos, grid.cell_size)
                entity_manager.get_character().update(event, turn_manager, mouse_pos)
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
                    grid_pos, pixel_pos = camera.apply_offset(event.pos, grid.cell_size)
                    entity_manager.get_character().targeting.handle_target_selection(grid_pos, grid, entity_manager.get_character().attacking, entity_manager.get_character(), turn_manager)
        if event.type == pygame.MOUSEWHEEL:
            grid.cell_size += event.y
            entity_manager.get_character().update_size(grid)
            entity_manager.get_character().movement.set_position(*entity_manager.get_character().grid_position)
            for enemy in entity_manager.get_enemies():
                enemy.update_size(grid)
                enemy.movement.set_position(*enemy.grid_position)
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN and turn_manager.is_in_combat():
            turn_manager.end_turn()
        if event.type == pygame.KEYUP and event.key == pygame.K_F1:
            logger.toggle()
        if event.type == pygame.KEYUP and event.key == pygame.K_F2:
            logger.clear_logs()
        if event.type == pygame.KEYUP and event.key == pygame.K_BACKQUOTE:  # Klawisz `~`
            command = input("Enter debug command: ")
            debug_console.handle_command(command)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Przesuń kamerę w górę
            camera.move(0, camera.speed)
        if keys[pygame.K_s]:  # Przesuń kamerę w dół
            camera.move(0, -camera.speed)
        if keys[pygame.K_a]:  # Przesuń kamerę w lewo
            camera.move(camera.speed, 0)
        if keys[pygame.K_d]:  # Przesuń kamerę w prawo
            camera.move(-camera.speed, 0)
        
            

def draw() -> None:
    gameScreen.fill(get_color("black"))
    grid.renderer.render(gameScreen, camera.offset)
    if entity_manager.get_character().health.is_alive():
        entity_manager.get_character().draw(gameScreen, camera.offset)
    for enemy in entity_manager.get_enemies():
        enemy.draw(gameScreen, camera.offset)

    entity_manager.get_character().pathfinder.draw_path(gameScreen, grid.cell_size, camera.offset)

    log_overlay.draw_logs(gameScreen, logger.logs)
    log_overlay.draw_fps(gameScreen, clock)

    if entity_manager.get_character().health.is_alive():
        menu.draw(gameScreen)
    turn_info.draw()
    level_up_ui.draw()
    console.draw(gameScreen)
    inventory_menu.draw_menu()
    pygame.display.flip()

while gameActive:
    draw()
    handle_events()
    turn_manager.check_combat_trigger(entity_manager.get_character(), entity_manager.get_enemies(), rooms, combat)
    clock.tick(framerate)

pygame.quit()



