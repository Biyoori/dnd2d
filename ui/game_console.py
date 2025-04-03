import pygame

pygame.font.init()

class GameConsole:
    def __init__(self, width, height, font_size=20, max_lines=5, bg_alpha=180) -> None:
        self.width = width
        self.height= height
        self.font_size = font_size
        self.max_lines = max_lines
        self.messages = []
        self.font = pygame.font.Font("Assets/UI/Fonts/IM_Fell_DW_Pica/IMFellDWPica-Regular.ttf", self.font_size)
        self.bg_color = (0, 0, 0, bg_alpha)
        self.text_color = (255, 255, 255)

        self.console_surface = pygame.Surface((self.width, self.font_size * self.max_lines), pygame.SRCALPHA)

    def log(self, message: str) -> None:
        self.messages.append(message)
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)
    
    def draw(self, screen: pygame.Surface):
        self.console_surface.fill(self.bg_color)

        y = 5
        for message in self.messages:
            text_surface = self.font.render(message, True, self.text_color)
            self.console_surface.blit(text_surface, (10, y))
            y += self.font_size
        screen.blit(self.console_surface, (0, self.height))

console = GameConsole(800, 500)