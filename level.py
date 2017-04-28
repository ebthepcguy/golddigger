from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect

import characters
import blocks
from debugDisplay import DebugDisplay
from hud import Hud

class Level(Scene):

    AIR_LEVEL = 3

    def __init__(self):
        super().__init__()

    def load(self):

        self.__player = characters.Player(3,1)
        self.addGameObject(DebugDisplay(0, self.game.height - 6))

        self.__gameArea = Rect(self.game.width, self.game.height - 9, 0, 0)
        self.generate(self.__gameArea.width, self.__gameArea.height)

        self.addGameObject(Hud(0, self.__gameArea.height))
        self.addGameObject(characters.Enemy(15,3))


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
