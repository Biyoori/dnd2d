import pygame
from core.event import Event
from entities.character.character import Character
from settings import get_color

class InventoryMenu:
    def __init__(self, font: pygame.font.Font, screen: pygame.Surface) -> None:
        self.active = False
        self.font = font
        self.buttons = []
        self.screen = screen
        self.hovered_button = None

        Event.subscribe("open_inventory", self.toggle_menu)
        

    def draw_menu(self, ) -> None:        
        if not self.active:
            return
        
        y_offset = 50
        menu_height = max(10 + len(self.inventory) * 30, 100)

        pygame.draw.rect(self.screen, get_color("dark-gray"), (50, 50, 300, menu_height), border_radius=5)
        pygame.draw.rect(self.screen, get_color("gold"), (50, 50, 300, menu_height), 1, border_radius=5)

        for rect, item in self.buttons:
            button_color = get_color("charcoal") if rect == self.hovered_button else get_color("dark-gray")
            pygame.draw.rect(self.screen,button_color, rect)

            text_surface = self.font.render(item.name, True, (255, 255, 255))
            self.screen.blit(text_surface, (rect.x, rect.y))
            y_offset += 50

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, item in self.buttons:
                if rect.collidepoint(event.pos):
                    print(f"Selected item: {item.name}")
                    if item.item_type == "weapon":
                        if Event.notify("use_action"):
                            Event.notify("equip_weapon", item)
                            print(f"Equipped weapon: {item.name}")
                    self.close()
                    break
        if event.type == pygame.MOUSEMOTION:
            for rect, item in self.buttons:
                if rect.collidepoint(event.pos):
                    # Handle hover effect here
                    self.hovered_button = rect
                    break

    def toggle_menu(self, player: "Character") -> None:
        self.active = not self.active
        if self.active:
            print("Inventory menu opened.")
        else:
            print("Inventory menu closed.")

        self.inventory = player.inventory.get_inventory()
        for index, item in enumerate(self.inventory):
            rect = pygame.Rect(60, 57 + index * 30, 280, 25)
            self.buttons.append((rect, item))

    def close(self) -> None:
        self.active = False
        self.buttons.clear()
        self.hovered_button = None

