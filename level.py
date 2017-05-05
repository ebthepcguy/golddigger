from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect
from engine.keyboard import Keyboard, KeyCode
from engine.popup import Popup

import characters, blocks, menu, time
from debugDisplay import DebugDisplay
from hud import Hud


class Level(Scene):

    AIR_LEVEL = 3

    def __init__(self):
        super().__init__()
        self.__popup = Popup("Save Game", "Load Game", "QUIT to Main Menu")
        self.__player = None
        self.__gameAria = None

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, player):
        self.__player = player

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
                    game.loadScene(menu.MainMenu())

    def load(self):
        super().load()
        self.__gameArea = Rect(self.game.width, self.game.height - 9, 0, 0)

        # If there are playerSpawn blocks
        if ( self.hasAny(blocks.PlayerSpawn) ):
            # Get the location of the block
            playerSpawn = self.getGameObjectsByType(blocks.PlayerSpawn)
            # Create a player if there is not one already
            if not ( self.__player ):
                self.__player = characters.Player(0, 0)
            # Spawn the player on the block
            self.__player.x = playerSpawn[0].x
            self.__player.y = playerSpawn[0].y
            self.removeGameObjectsByType(blocks.PlayerSpawn)
            self.addGameObject(self.__player)
        # If there are not Player Objects create one
        elif ( not self.hasAny(characters.Player) ):
            if not ( self.__player ):
                self.__player = characters.Player(0,0)
            self.__player.x = 3
            self.__player.y = 1
            self.addGameObject(self.__player)
        # If there are Player Objects
        elif ( self.hasAny(characters.Player) ):
            self.__player = self.getGameObjectsByType(characters.Player)[0]

        self.addGameObject(DebugDisplay(0, self.game.height - 6))

        self.addGameObject(Hud(0, self.__gameArea.height))

        self.originalGos = self.gameObjects

    # to delete
    def getPlayer(self):
        return self.__player

    def getGameArea(self):
        return self.__gameArea

    def generate(self):
        width = Game.Width
        height = Game.Height - 9

        # Build base layer of air and stone
        for row in range(0, height):
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

        # Add player
        #self.addGameObject(self.__player)

    def saveGameMenu(self, game):

        self.paused = False
        self.removeGameObjectsByType(Popup)

        saveMenu = menu.SaveMenu("Save Your Game: Enter a name.", self)
        saveMenu.fileName = menu.Menu.GAME_FILE
        game.loadScene(saveMenu)

    def loadGameMenu(self, game):

        self.paused = False
        self.removeGameObjectsByType(Popup)

        loadMenu = menu.LoadMenu("Load Game:", self)
        loadMenu.fileName = menu.Menu.GAME_FILE
        game.loadScene(loadMenu)
