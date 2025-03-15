from core.settings import *
from core.grid import Grid
from ui.characterCreatorLoop import runCharacterCreator

pygame.init()

gameScreen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

testCharacter = runCharacterCreator(gameScreen)
print(f"Created: ")
testCharacter.displayCharacterInfo()
print(testCharacter.race)

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



