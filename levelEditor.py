from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect
from engine.keyboard import Keyboard, KeyCode

import characters, blocks, menu
from popup import Popup
from debugDisplay import DebugDisplay
from hud import Hud

class LevelEditor(Scene):

    AIR_LEVEL = 5

    def __init__(self):
        super().__init__()
        self.__popup = Popup("Save Level", "Load Level", "QUIT to Main Menu")

    def load(self):
        super().load()

        blockWidth = blocks.Block.width
        blockHeight = blocks.Block.height
        self.gameArea = Rect(Game.curGame.width - blockWidth, Game.curGame.height - Hud.height, 0, 0)

        if ( self.len() == 0 ):
            self.generateMap()

        playerStartX = blockWidth
        playerStartY = blockHeight

        self.player = characters.EditCursor(playerStartX, playerStartY)
        # Add player
        self.addGameObject(self.player, 1)

    def update(self):
        kb = Game.curGame.keyboard

        if (kb.keyPressed(KeyCode.ESC)):
            if self.paused:
                self.paused = False
                self.removeGameObjectsByType(Popup)
            else:
                self.paused = True
                self.addGameObject(self.__popup)

        if self.hasAny(Popup):
            if (kb.keyPressed(KeyCode.ENTER)):
                activeOption = self.__popup.activeOption

                if activeOption == 0:
                    self.startSaveLevelMenu()
                elif activeOption == 1:
                    self.startLoadLevelMenu()
                elif activeOption == 2:
                    Game.curGame.loadScene(menu.MainMenu())

    def generateOld(self, width, height):

        for row in range(0,height):
            for col in range(0, width * 3, 3):
                if (row == 0):
                    block = blocks.Wall(col, row)
                elif ( col == 0 or col == width - 3):
                    block = blocks.Wall(col, row)
                elif (row == height - 1):
                    if(col == int(width / 3) -1):
                        block = blocks.Door(col, row)
                    else:
                        block = blocks.Wall(col, row)
                else:
                    block = blocks.Dirt(col, row)

                self.addGameObject(block)

    def generateMap(self):
        blockWidth = 3
        blockHeight = 1
        levelWidth = self.gameArea.width
        levelHeight = self.gameArea.height
        startX = self.gameArea.x
        startY = self.gameArea.y

        doorYPos = 7

        for y in range(startY, levelHeight + blockHeight, blockHeight):
            for x in range(startX, levelWidth + blockWidth, blockWidth):
                if ( y == startY or x == startX or x == levelWidth or y == levelHeight ):
                    if( x == blockWidth * doorYPos and y == levelHeight ):
                        block = blocks.Door(x, y)
                    else:
                        block = blocks.Wall(x, y)
                else:
                    block = blocks.Dirt(x, y)

                self.addGameObject(block)

    def startSaveLevelMenu(self):

        self.paused = False
        self.removeGameObjectsByType(characters.EditCursor)
        self.removeGameObjectsByType(Popup)

        saveMenu = menu.SaveMenu("Save Your Custom Level: Enter a name.", self)
        saveMenu.fileName = menu.Menu.LEVEL_FILE
        Game.curGame.loadScene(saveMenu)

    def startLoadLevelMenu(self):

        self.paused = False
        self.removeGameObjectsByType(characters.EditCursor)
        self.removeGameObjectsByType(Popup)

        loadMenu = menu.LoadMenu("Load Custom Level:", self)
        loadMenu.fileName = menu.Menu.LEVEL_FILE
        Game.curGame.loadScene(loadMenu)
