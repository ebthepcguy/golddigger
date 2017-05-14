from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect
from engine.keyboard import Keyboard, KeyCode
from engine.image import Image

import characters, blocks, menu, time
from popup import Popup
from debugDisplay import DebugDisplay
from hud import Hud


class Level(Scene):

    MAX_LEVEL = 3

    def __init__(self):
        super().__init__()
        self.__popup = Popup("Save Game", "Load Game", "QUIT to Main Menu")

    def load(self):
        super().load()

        blockWidth = blocks.Block.width
        blockHeight = blocks.Block.height
        self.gameArea = Rect(Game.curGame.width - blockWidth, Game.curGame.height - Hud.height, 0, 0)

        playerStartX = blockWidth
        playerStartY = blockHeight

        # If there are playerSpawn blocks
        if ( self.hasAny(blocks.PlayerSpawn) ):
            # Get the location of the block
            playerSpawn = self.getGameObjectsByType(blocks.PlayerSpawn)
            # Create a player if there is not one already
            if not ( self.player ):
                self.player = characters.Player(playerStartX, playerStartY)
            # Spawn the player on the block
            self.player.x = playerSpawn[0].x
            self.player.y = playerSpawn[0].y
            self.removeGameObjectsByType(blocks.PlayerSpawn)
            self.addGameObject(self.player)
        # If there are not Player Objects create one
        elif ( not self.hasAny(characters.Player) ):
            if not ( self.player ):
                self.player = characters.Player(0, 0)
            self.player.x = playerStartX
            self.player.y = playerStartY
            self.addGameObject(self.player)
        # If there are Player Objects
        elif ( self.hasAny(characters.Player) ):
            self.player = self.getGameObjectsByType(characters.Player)[0]

        self.addGameObject(Hud(blockWidth, self.gameArea.height + blockHeight))

        self.originalGos = self.gameObjects

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
                    self.saveGameMenu()
                elif activeOption == 1:
                    self.loadGameMenu()
                elif activeOption == 2:
                    Game.curGame.loadScene(menu.MainMenu())

    def generateMap(self):

        blockWidth = 3
        blockHeight = 1

        self.gameArea = Rect(Game.curGame.width - blockWidth, Game.curGame.height - Hud.height, 0, 0)

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

    def saveGameMenu(self):

        self.paused = False
        self.removeGameObjectsByType(Popup)

        saveMenu = menu.SaveMenu("Save Your Game: Enter a name.", self)
        saveMenu.fileName = menu.Menu.GAME_FILE
        Game.curGame.loadScene(saveMenu)

    def loadGameMenu(self):

        self.paused = False
        self.removeGameObjectsByType(Popup)

        loadMenu = menu.LoadMenu("Load Game:", self)
        loadMenu.fileName = menu.Menu.GAME_FILE
        Game.curGame.loadScene(loadMenu)
