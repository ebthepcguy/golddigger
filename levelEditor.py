from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect
from engine.keyboard import Keyboard, KeyCode
from engine.popup import Popup

import characters, blocks, mainMenu
from debugDisplay import DebugDisplay

class LevelEditor(Scene):

    AIR_LEVEL = 5

    def __init__(self):
        super().__init__()
        self.__popup = Popup("Save Level", "Load Level", "QUIT to Main Menu")

    def update(self, game):
        kb = game.keyboard

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
                    self.startSaveLevelMenu(game)
                elif activeOption == 1:
                    self.startLoadLevelMenu(game)
                elif activeOption == 2:
                    game.loadScene(mainMenu.MainMenu())

    def load(self):
        self.__gameArea = Rect(self.game.width, self.game.height - 9, 0, 0)
        self.__player = characters.EditCursor(3, 0)
        if ( self.len() == 0 ):
            self.generate(self.__gameArea.width, self.__gameArea.height)
        self.addGameObject(DebugDisplay(0, self.game.height - 6))
        # Add player
        self.addGameObject(self.__player, 1)

    def getPlayer(self):
        return self.__player

    def getGameArea(self):
        return self.__gameArea

    def generate(self, width, height):

        for row in range(0,height):
            for col in range(0, width * 3, 3):
                if (row == 0):
                    block = blocks.Wall(col, row)
                elif ( col == 0 or col == width - 3):
                    block = blocks.Wall(col, row)
                elif (row in range(0, self.AIR_LEVEL)):
                    pass
                elif (row == height - 1):
                    if(col == int(width / 3) -1):
                        block = blocks.Door(col, row)
                    else:
                        block = blocks.Wall(col, row)
                else:
                    block = blocks.Dirt(col, row)

                self.addGameObject(block)

    def startSaveLevelMenu(self, game):
        import saveMenu

        self.paused = False
        self.removeGameObjectsByType(characters.EditCursor)
        self.removeGameObjectsByType(Popup)

        saveMenu = saveMenu.SaveMenu("Save Level: Choose your name.", game.SAVE_FOLDER + "/levels", self)
        game.loadScene(saveMenu)

    def startLoadLevelMenu(self, game):
        import loadMenu

        self.paused = False
        self.removeGameObjectsByType(characters.EditCursor)
        self.removeGameObjectsByType(Popup)

        loadMenu = loadMenu.LoadMenu("Load Level: Choose a level.", game.SAVE_FOLDER + "/levels", self)
        game.loadScene(loadMenu)
