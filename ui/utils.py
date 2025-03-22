import pygame
from settings import getColorFromPallette

pygame.font.init()
font = pygame.font.Font(None, 40)

def drawText(content: str, x: int, y: int, screen: pygame.Surface, color=getColorFromPallette("white"), alignLeft=0):
        textToDraw = font.render(content, True, color)
        if alignLeft:
            textSize = textToDraw.get_rect(midleft=(x, y))
        else:
            textSize = textToDraw.get_rect(center=(x, y))
        screen.blit(textToDraw, textSize)