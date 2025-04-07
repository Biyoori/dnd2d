import pygame
from core.event import Event
from settings import get_color
from ui.character_creator.data.classes import get_classes

class ClassSelectionUI:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.screen = screen
        self.font = font
        self.classes = get_classes()
        self.selected_class = None
        self.active = False

        self.popup_rect = pygame.Rect(50, 50, 250, 200)

        self.buttons = []
        for i, cls in enumerate(self.classes):
            rect = pygame.Rect(70, 80 + i * 50, 200, 40)
            self.buttons.append((rect, cls))

        Event.subscribe("show_class_selection_ui", self.show)

    def show(self) -> None:
        self.active = True

    def draw(self) -> None:
        if not self.active:
            return
        
        pygame.draw.rect(self.screen, get_color("dark-gray"), self.popup_rect, border_radius=5)
        pygame.draw.rect(self.screen, get_color("gold"), self.popup_rect, 1, 3)

        for rect, cls in self.buttons:
            pygame.draw.rect(self.screen, (50, 50, 50), rect, border_radius=5)
            pygame.draw.rect(self.screen, get_color("gold"), rect, 1, 5)
            text = self.font.render(cls.name, True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 20, rect.y + 5))

    def handle_event(self, event) -> None:
        if not self.active:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, cls in self.buttons:
                if rect.collidepoint(event.pos):
                    self.selected_class = cls
                    self.active = False
                    Event.notify("class_selected", cls)