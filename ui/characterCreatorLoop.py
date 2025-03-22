import pygame
from ui.characterCreator import CharacterCreator

def runCharacterCreator(screen: pygame.Surface):
    creatorActive = True

    ch = CharacterCreator(screen)

    while creatorActive:
        
        screen.fill("black")
        
        ch.drawCreationSteps()
        ch.eventHandler()
        
        pygame.display.flip()
        if not ch.status:
            character = ch.createCharacter()
            creatorActive = False
            

    return character