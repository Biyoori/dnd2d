from settings import *
from core.grid import Grid
from ui.characterCreatorLoop import runCharacterCreator
from combat.combat import Combat
from combat.turnManager import TurnManager
from movement.movementManager import MovementManager
from factories.enemyFactory import EnemyFactory

pygame.init()

gameScreen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

enemyFactory = EnemyFactory("data/enemies")
movementManager = MovementManager()
turnManager = TurnManager(movementManager)

testCharacter = runCharacterCreator(gameScreen)
skeleton = enemyFactory.createEnemy("skeleton")

#testcombat = runCharacterCreator(gameScreen)
print(f"Created: ")
testCharacter.displayCharacterInfo()
print(testCharacter.race)

gameActive = True
grid = Grid()

skeleton.initialize(5,5,grid,movementManager)
testCharacter.initialize(1, 1, grid, movementManager)
#testcombat.initialize(5, 5, grid, turnManager, movementManager)


combat = Combat([testCharacter], [], turnManager)
turnManager.startCombat(combat)

skeleton.executeAction("Shortsword", testCharacter)

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
    skeleton.draw(gameScreen)
    #testcombat.draw(gameScreen)
    pygame.display.flip()

while gameActive:
    handle_events()
    draw()
    clock.tick(framerate)

pygame.quit()



