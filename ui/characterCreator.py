import pygame
from enum import Enum 
from core.settings import screenHeight, screenWidth, getColorFromPallette
from characters.characterFactory import CharacterFactory
from characters.classes import Barbarian, Fighter
from characters.race import Race
from core.utils import loadJson

pygame.font.init()
font = pygame.font.Font(None, 40)
center = pygame.Vector2(screenWidth/2, screenHeight/2)

class OptionsOfCharacterClasses(Enum):
    BARBARIAN = Barbarian()
    FIGHTER = Fighter()

CHARACTER_CLASSES = list(OptionsOfCharacterClasses)

class CharacterCreator:
    def __init__(self, screen):                
        self.RACES_DATA = loadJson("characters/races.json")
        self.RACES = list(self.RACES_DATA.keys())
        self.ABILITY_SCORE_NAMES = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        self.screen = screen
        self.creationStep = "Name Step"
        self.characterName = ""
        self.selectedRace = None
        self.selectedClassIndex = 0
        self.selectedRaceIndex = 0
        self.abilityScores = {name: 8 for name in reversed(self.ABILITY_SCORE_NAMES)}
        self.selectedAbility=0
        self.abilityScorePoints=27
        self.skillProficiencyOptions = []
        self.skillProficienciesSelected = {}
        self.selectedSkill = 0
        self.skillPoints = 0
        self.status = 1
        

    def drawText(self, content: str, x: int, y: int, color=getColorFromPallette("white"), alignLeft=0):
        textToDraw = font.render(content, True, color)
        if alignLeft:
            textSize = textToDraw.get_rect(midleft=(x, y))
        else:
            textSize = textToDraw.get_rect(center=(x, y))
        self.screen.blit(textToDraw, textSize)
       
    def calculateAbilityCost(self, abilityScore):
        return (abilityScore - (abilityScore - 1)) + (abilityScore >= 14)

    def getSelectedClass(self):
        return CHARACTER_CLASSES[self.selectedClassIndex]
    
    def getSelectedAbility(self):
        return self.abilityScores[self.ABILITY_SCORE_NAMES[self.selectedAbility]]
    
    def setSelectedAbility(self, value: int):
        self.abilityScores[self.ABILITY_SCORE_NAMES[self.selectedAbility]] = max(8, min(value, 15))

    def createSkillProficiencyDict(self):
        return {skill: False for skill in self.getSelectedClass().value.startingSkillProficiencyOptions}
    
    def getSelectedSkillName(self):
        return self.skillProficiencyOptions[self.selectedSkill]
    
    def setSelectedSkill(self):
        self.skillProficienciesSelected[self.getSelectedSkillName()] = not self.skillProficienciesSelected[self.getSelectedSkillName()]

    def getSelectedSkill(self):
        return self.skillProficienciesSelected[self.getSelectedSkillName()]

    def drawNameStep(self):
        self.drawText("Enter characters name", center.x, center.y-40)
        pygame.draw.rect(self.screen, getColorFromPallette("light-gray"), (center.x-120,center.y-20,240,40), 2)
        pygame.draw.rect(self.screen, getColorFromPallette("black"), (center.x-110,center.y-15, 220, 30))
        self.drawText(f"{self.characterName}", *center)

    def drawClassStep(self):
        self.drawText("Pick a class", center.x, center.y-40)
        self.drawText(f"< {self.getSelectedClass().value.name} >", *center)

    def drawRaceStep(self):
        self.drawText("Pick a race", center.x, center.y-40)
        self.drawText(f"< {self.RACES[self.selectedRaceIndex]} >", *center)

    def drawAbilityStep(self):
        bonuses = self.selectedRace.abilityScoreBonuses.copy()
        self.drawText(f"Select ability scores: {self.abilityScorePoints}", center.x, center.y-40)
        drawHeight = -180
        xOffset = 114
        for name, score in self.abilityScores.items():
            if name == self.ABILITY_SCORE_NAMES[self.selectedAbility]:
                self.drawText(f"< {name}: {score} >", center.x-xOffset, center.y-drawHeight, alignLeft=1)
            else:
                self.drawText(f"{name}: {score}", center.x-90, center.y-drawHeight, alignLeft=1)
            if name in bonuses:
                self.drawText(f"+{bonuses[name]}", center.x+160, center.y-drawHeight)
                bonuses.pop(name)
            drawHeight+= 35

    def drawSkillStep(self):
        drawHeight = -5
        self.drawText(f"Choose skill proficiencies: {self.skillPoints}", center.x, center.y-40)
        for skill, selected in self.skillProficienciesSelected.items():
            if skill == self.getSelectedSkillName():
                self.drawText(f"< {skill} >", center.x-160, center.y-drawHeight, alignLeft=1)
            else:
                self.drawText(f"{skill}", center.x-160, center.y-drawHeight, alignLeft=1)
            if selected:
                self.drawText("x", center.x+160, center.y-drawHeight)
            drawHeight-= 35

    def drawCreationSteps(self):
        match self.creationStep:
            case "Name Step":
                self.drawNameStep()
            case "Class Step":
                self.drawClassStep()
            case "Race Step":
                self.drawRaceStep()
            case "Ability Step":
                self.drawAbilityStep()
            case "Skill Step":
                self.drawSkillStep()

    def eventHandler(self):

        def handleNameStepKeyDown(event: pygame.event):          
            if len(self.characterName) < 12 and event.key != 8:
                self.characterName += event.unicode        

        def handleNameStepBackspace(event):
            self.characterName = self.characterName[:-1]

        def handleNameStepReturn(event):
            self.creationStep = "Class Step"

        def handleClassStepKeyRight(event):
            self.selectedClassIndex = (self.selectedClassIndex + 1) % len(CHARACTER_CLASSES)

        def handleClassStepKeyLeft(event):
            self.selectedClassIndex = (self.selectedClassIndex - 1) % len(CHARACTER_CLASSES)

        def handleClassStepReturn(event):
            self.skillProficienciesSelected = self.createSkillProficiencyDict()
            self.skillProficiencyOptions = self.getSelectedClass().value.startingSkillProficiencyOptions
            self.skillPoints = self.getSelectedClass().value.startingSkillProficiencies
            self.creationStep = "Race Step"

        def handleRaceStepKeyRight(event):
            self.selectedRaceIndex = (self.selectedRaceIndex + 1) % len(self.RACES)

        def handleRaceStepKeyLeft(event):
            self.selectedRaceIndex = (self.selectedRaceIndex - 1) % len(self.RACES)
        
        def handleRaceStepReturn(event):
            self.selectedRace = Race(self.RACES[self.selectedRaceIndex], self.RACES_DATA[self.RACES[self.selectedRaceIndex]])
            self.creationStep = "Ability Step"

        def handleAbilityStepKeyDown(event):
            self.selectedAbility = (self.selectedAbility + 1) % len(self.ABILITY_SCORE_NAMES)

        def handleAbilityStepKeyUp(event):
            self.selectedAbility = (self.selectedAbility - 1) % len(self.ABILITY_SCORE_NAMES)

        def handleAbilityStepKeyRight(event):
            nextCost = self.calculateAbilityCost(self.getSelectedAbility()+1)
            if(self.abilityScorePoints >= nextCost) and self.getSelectedAbility() < 15:
                self.abilityScorePoints -= nextCost
                self.setSelectedAbility(self.getSelectedAbility()+1)

        def handleAbilityStepKeyLeft(event):
            cost = self.calculateAbilityCost(self.getSelectedAbility())
            if self.abilityScorePoints < 27 and self.getSelectedAbility() > 8:
                self.abilityScorePoints += cost
                self.setSelectedAbility(self.getSelectedAbility()-1)

        def handleAbilityStepReturn(event):
            if self.abilityScorePoints <= 0:
                self.abilityScores = self.selectedRace.applyAbilityBonuses(self.abilityScores)
                self.creationStep = "Skill Step"         

        def handleSkillStepDown(event):
            self.selectedSkill = (self.selectedSkill + 1) % len(self.skillProficiencyOptions)

        def handleSkillStepUp(event):
            self.selectedSkill = (self.selectedSkill - 1) % len(self.skillProficiencyOptions)

        def handleSkillStepRight(event):
            if self.skillPoints > 0 and not self.getSelectedSkill():
                self.setSelectedSkill()
                self.skillPoints -= 1
            elif self.skillPoints <= self.getSelectedClass().value.startingSkillProficiencies and self.getSelectedSkill():
                self.setSelectedSkill()
                self.skillPoints += 1

        def handleSkillStepReturn(event):
            if self.skillPoints <= 0:
                self.status = 0

        stepEventHandlers = {
            "Name Step": {
                pygame.KEYDOWN: handleNameStepKeyDown,
                pygame.K_BACKSPACE: handleNameStepBackspace,
                pygame.K_RETURN: handleNameStepReturn
            },
            "Class Step": {
                pygame.K_RIGHT: handleClassStepKeyRight,
                pygame.K_LEFT: handleClassStepKeyLeft,
                pygame.K_RETURN: handleClassStepReturn
            },
            "Race Step": {
                pygame.K_RIGHT: handleRaceStepKeyRight,
                pygame.K_LEFT: handleRaceStepKeyLeft,
                pygame.K_RETURN: handleRaceStepReturn
            },
            "Ability Step": {
                pygame.K_DOWN: handleAbilityStepKeyDown,
                pygame.K_UP: handleAbilityStepKeyUp,
                pygame.K_RIGHT: handleAbilityStepKeyRight,
                pygame.K_LEFT: handleAbilityStepKeyLeft,
                pygame.K_RETURN: handleAbilityStepReturn
            },
            "Skill Step": {
                pygame.K_DOWN: handleSkillStepDown,
                pygame.K_UP: handleSkillStepUp,
                pygame.K_RIGHT: handleSkillStepRight,
                pygame.K_RETURN: handleSkillStepReturn
            }
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type in [pygame.KEYDOWN]:

                handler = stepEventHandlers.get(self.creationStep, {}).get(event.key)
                if handler:
                    handler(event)

                handler = stepEventHandlers.get(self.creationStep, {}).get(event.type)
                if handler:
                    handler(event)
            else:
                handler = stepEventHandlers.get(self.creationStep, {}).get(event.type)
                if handler:
                    handler(event)
            
    def createCharacter(self):
        classes = [self.getSelectedClass().value]
        skillProficienciesSelected = [skill for skill, selected in self.skillProficienciesSelected.items() if selected is True]
        return CharacterFactory.createCharacter(self.characterName, classes, self.selectedRace, self.abilityScores, skillProficienciesSelected)