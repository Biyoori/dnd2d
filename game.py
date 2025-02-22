from settings import *
from core.grid import Grid
from characters.character import Character
from ui.characterCreator import runCharacterCreator
from characters.classes import Barbarian

pygame.init()

#Inicjalizacja
gameScreen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

playerStartPoint = pygame.Vector2(1, 1)

testCharacter = runCharacterCreator(gameScreen)

print("Created: " + str(testCharacter))

gameActive = True
grid = Grid()
testCharacter.setPosition(1,1,grid.cellSize)

def handle_events():
    global gameActive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False

def draw():
    gameScreen.fill(getColorFromPallette("black"))
    grid.draw(gameScreen, getColorFromPallette("gray"))
    testCharacter.draw(gameScreen)
    pygame.display.flip()

while gameActive:
    handle_events()
    draw()
    clock.tick(framerate)

pygame.quit()


