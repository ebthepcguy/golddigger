from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect
from engine.keyboard import Keyboard, KeyCode
from engine.popup import Popup

import characters
import blocks
from debugDisplay import DebugDisplay

class LevelEditor(Scene):

    AIR_LEVEL = 5

    def __init__(self):
        super().__init__()
        self.__popup = Popup("Save Level", "Load Level", "QUIT")

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
                    pass
                elif activeOption == 2:
                    game.quit()

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
                    block = blocks.Air(col, row)
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

        saveMenu = saveMenu.SaveMenu("Save Level: Choose your name.", self, "levels/levels")
        game.loadScene(saveMenu)




