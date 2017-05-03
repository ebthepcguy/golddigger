from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect
from engine.keyboard import Keyboard, KeyCode
from engine.popup import Popup

import characters, blocks, mainMenu, time
from debugDisplay import DebugDisplay
from hud import Hud


class Level(Scene):

    AIR_LEVEL = 3

    def __init__(self):
        super().__init__()
        self.__popup = Popup("Save Game", "Load Game", "QUIT to Main Menu")

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
                    self.saveGameMenu(game)
                elif activeOption == 1:
                    self.loadGameMenu(game)
                elif activeOption == 2:
                    game.loadScene(mainMenu.MainMenu())

    def load(self):
        self.__gameArea = Rect(self.game.width, self.game.height - 9, 0, 0)

        if ( self.hasAny(blocks.PlayerSpawn) ):
            playerSpawn = self.getGameObjectsByType(blocks.PlayerSpawn)
            self.__player = characters.Player(playerSpawn[0].x, playerSpawn[0].y)
            self.removeGameObjectsByType(blocks.PlayerSpawn)
            self.addGameObject(self.__player)
        elif ( not self.hasAny(characters.Player) ):
            self.__player = characters.Player(3,1)
            self.addGameObject(self.__player)
        elif ( self.hasAny(characters.Player) ):
            self.__player = self.getGameObjectsByType(characters.Player)[0]

        self.addGameObject(DebugDisplay(0, self.game.height - 6))

        self.addGameObject(Hud(0, self.__gameArea.height))

    def getPlayer(self):
        return self.__player

    def getGameArea(self):
        return self.__gameArea

    def generate(self, width, height):

        # Build base layer of air and stone
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

        # Add player
        self.addGameObject(self.__player)

        # to test some thing out

        block = blocks.Stone(3, 0)
        self.addGameObject(block)

        block = blocks.Stone(3, 3)
        self.addGameObject(block)

    def saveGameMenu(self, game):
        import saveMenu

        self.paused = False
        self.removeGameObjectsByType(Popup)

        saveMenu = saveMenu.SaveMenu("Save Game: Choose your name.", game.SAVE_FOLDER + "/games", self)
        game.loadScene(saveMenu)

    def loadGameMenu(self, game):
        import loadMenu

        self.paused = False
        self.removeGameObjectsByType(Popup)

        loadMenu = loadMenu.LoadMenu("Load Game: Choose a game.", game.SAVE_FOLDER + "/games", self)
        game.loadScene(loadMenu)
