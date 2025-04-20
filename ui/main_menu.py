import pygame
from settings import font_path, screen_width, screen_height
from debugging import logger

class MainMenu:
    def __init__(self, screen):
        self.options = {
            "0": "Start Game",
            "1": "Load Game",
            "2": "Settings",
            "3": "Exit"
        }
        self.selected_option = 0
        self.font = pygame.font.Font(font_path, 80)
        self.screen = screen
        self.running = True

    def display_menu(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            self.screen.fill((0, 0, 0))

            self.draw_menu()
            self.handle_events()

            pygame.display.flip()
            clock.tick(30)

    def draw_menu(self) -> None:
        y_offset = 80
        for key, value in self.options.items():
            if int(key) == self.selected_option:
                text_surface = self.font.render(f"> {value} <", True, (255, 255, 0))
            else:
                text_surface = self.font.render(value, True, (255, 255, 255))
            self.screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, text_surface.get_height() + y_offset))
            y_offset += 80
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.execute_option(self.selected_option)

    def execute_option(self, option: int) -> None:
        if option == 0:
            logger.log("Starting game...", "INFO")
            self.running = False
        elif option == 1:
            logger.log("Loading game...", "INFO")
            # Add logic to load a game
        elif option == 2:
            logger.log("Opening settings...", "INFO")
            # Add logic to open settings
        elif option == 3:
            logger.log("Exiting...", "INFO")
            self.running = False
            pygame.quit()
            