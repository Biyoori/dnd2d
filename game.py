from settings import *
from core.grid import Grid
from ui.characterCreatorLoop import runCharacterCreator
from combat.combat import Combat
from combat.turnManager import TurnManager
from movement.movementManager import MovementManager

pygame.init()

gameScreen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

movementManager = MovementManager()
turnManager = TurnManager(movementManager)

testCharacter = runCharacterCreator(gameScreen)
#testcombat = runCharacterCreator(gameScreen)
print(f"Created: ")
testCharacter.displayCharacterInfo()
print(testCharacter.race)

gameActive = True
grid = Grid()

testCharacter.initialize(1, 1, grid, movementManager)
#testcombat.initialize(5, 5, grid, turnManager, movementManager)


combat = Combat([testCharacter], [], turnManager)
turnManager.startCombat(combat)

def handle_events():
    global gameActive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False
        
        testCharacter.update(event, turnManager)
        #testcombat.update(event)

def draw():
    gameScreen.fill(getColorFromPallette("black"))
    grid.draw(gameScreen)
    testCharacter.draw(gameScreen)
    #testcombat.draw(gameScreen)
    pygame.display.flip()

while gameActive:
    handle_events()
    draw()
    clock.tick(framerate)

pygame.quit()



