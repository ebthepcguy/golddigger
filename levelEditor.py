from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.util import Rect

import characters
import blocks
from debugDisplay import DebugDisplay

class LevelEditor(Scene):

    AIR_LEVEL = 3

    def __init__(self):
        super().__init__()

    def load(self):
        #self.__player = characters.Player(0,0)
        self.__player = characters.EditCursor(3, 0)
        self.addGameObject(DebugDisplay(0, self.game.height - 6))
        self.__gameArea = Rect(self.game.width, self.game.height - 9, 0, 0)
        self.generate(0, self.__gameArea.width, self.__gameArea.height)

    def getPlayer(self):
        return self.__player

    def getGameArea(self):
        return self.__gameArea

    def generate(self, lvl, width, height):

        # Build base layer of air and stone
        for row in range(0,height):
            for col in range(0, width * 3, 3):
                if(lvl == 0 and row in range(0, self.AIR_LEVEL)):
                    block = blocks.Air(col, row)
                elif(row == height - 1):
                    if(col == int(width / 3) -1):
                        block = blocks.Door(col, row)
                    else:
                        block = blocks.Wall(col, row)
                else:
                    block = blocks.Dirt(col, row)

                self.addGameObject(block)

        # Add player
        self.addGameObject(self.__player, 1)

