from .debug_logger import logger
import pygame

class DebugOverlay:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font
    
    def draw_logs(self, screen: pygame.Surface, logs: list[str]) -> None:
        if not logger.debug_mode:
            return
        
        y_offset = 10
        for log in logger.logs[-10:]:
            text_surface = self.font.render(log, True, (255, 255, 255))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 20

    def draw_fps(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        if not logger.debug_mode:
            return
        
        fps = int(clock.get_fps())
        text_surface = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 50))