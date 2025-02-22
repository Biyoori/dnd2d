import pygame
import json
from enum import Enum
from settings import screenHeight, screenWidth, getColorFromPallette
from characterFactory import CharacterFactory
from characters.classes import Barbarian, Fighter
from race import Race

pygame.font.init()
font = pygame.font.Font(None, 40)
center = pygame.Vector2(screenWidth/2, screenHeight/2)

class OptionsOfCharacterClasses(Enum):
    BARBARIAN = Barbarian()
    FIGHTER = Fighter()

CHARACTER_CLASSES = list(OptionsOfCharacterClasses)


def drawText(content: str, x: int, y: int, screen: pygame.surface, color=getColorFromPallette("white")):
    textToDraw = font.render(content, True, color)
    textSize = textToDraw.get_rect(center=(x, y))
    screen.blit(textToDraw, textSize)

def loadRaces(filename="races.json"):
    with open(filename, "r", encoding="utf-8") as file:
        races = json.load(file)
        return races

def runCharacterCreator(screen: pygame.surface):
    creatorActive = True #??
    creationStep = 0 # 0=Name, 1=Class, 2=return
    characterName = ""
    selectedClassIndex = 0
    selectedRaceIndex = 0
    racesData = loadRaces()
    races = list(racesData.keys())
    while creatorActive:
        screen.fill("black")
        match creationStep:
            case 0:
                drawText("Enter characters name", center.x, center.y-40, screen)
                pygame.draw.rect(screen, getColorFromPallette("light-gray"), (center.x-120,center.y-20,240,40), 2)
                pygame.draw.rect(screen, getColorFromPallette("black"), (center.x-110,center.y-15, 220, 30))
                drawText(f"{characterName}", *center, screen)
            case 1:
                selectedClass = CHARACTER_CLASSES[selectedClassIndex]
                drawText("Pick a class", center.x, center.y-40, screen)
                drawText(f"< {selectedClass.value.name} >", *center, screen)  
            case 2:
                selectedRace = racesData[races[selectedClassIndex]]
                drawText("Pick a race", center.x, center.y-40, screen)
                drawText(f"< {races[selectedRaceIndex]} >", *center, screen)  
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if creationStep == 2:
                    if event.key == pygame.K_RETURN:
                        creationStep+=1
                    elif event.key == pygame.K_RIGHT:
                        selectedRaceIndex = (selectedRaceIndex + 1) % len(CHARACTER_CLASSES)
                    elif event.key == pygame.K_LEFT:
                        selectedRaceIndex = (selectedRaceIndex - 1) % len(CHARACTER_CLASSES)
                if creationStep == 1:
                    if event.key == pygame.K_RETURN:
                        creationStep+=1
                    elif event.key == pygame.K_RIGHT:
                        selectedClassIndex = (selectedClassIndex + 1) % len(CHARACTER_CLASSES)
                    elif event.key == pygame.K_LEFT:
                        selectedClassIndex = (selectedClassIndex - 1) % len(CHARACTER_CLASSES)
                if creationStep == 0:
                    if event.key == pygame.K_RETURN:
                        creationStep+=1
                    elif event.key == pygame.K_BACKSPACE:
                        characterName = characterName[:-1]
                    elif len(characterName) < 12:
                        characterName += event.unicode
            if creationStep == 3:
                    print(racesData[races[selectedRaceIndex]])
                    print(races[selectedRaceIndex])
                    return CharacterFactory.createCharacter(characterName, selectedClass.value, Race(races[selectedRaceIndex], racesData[races[selectedRaceIndex]]))    
            
        
        pygame.display.flip()