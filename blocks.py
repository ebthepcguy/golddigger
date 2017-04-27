from engine.image import Image
from engine.tile import Tile
from engine.game import Game
from engine.gameObject import GameObject
import level
from engine.util import clamp

class Block(GameObject):
    def __init__(self, x, y, image, collision = True):
        super().__init__(x, y, image, collision)
        self.__game = None
        self.falling = False

    def update(self, game):
        self.__game = game


    ###########################################################################
    # This code is from characters. I would like to see all GameObjects get
    # this (or something like this) in the future.
    def fall(self):
        scene = self.__game.curScene

        if(isinstance(scene, level.Level)):
            gameArea = scene.getGameArea()

        x = clamp( self.x, gameArea.x, gameArea.width )
        y = clamp( self.y + 1, gameArea.y, gameArea.height )


        gameObjects = scene.getGameObjectsAtPos(x, y)

        canMove = True

        for gO in gameObjects:
            if(gO.collision):
                canMove = False

        if(canMove):
            self.x = x
            self.y = y

    def testFalling(self):
        scene = self.__game.curScene
        gameObjects = scene.getGameObjectsAtPos(self.x, self.y + 1)
        isFalling = True
        for gO in gameObjects:
            if(gO.collision):
                isFalling = False

        self.__falling = isFalling

    def isFalling(self):
        return self.__falling
    ##################################################################################

class Air(Block):
    def __init__(self, x, y):
        image = Image([[Tile("█"), Tile("█"), Tile("█")]])
        super().__init__(x, y, image, False)

class Dirt(Block):

    FULL = Image([[Tile("▒"), Tile("▒"), Tile("▒")]])
    HALF = Image([[Tile("░"), Tile("░"), Tile("░")]])


    def __init__(self, x, y, health = 2):
        image = self.FULL
        super().__init__(x, y, image)
        self.__health = health

    def setHealth(self, health):
        self.__health = health

    def getHealth(self):
        return self.__health

    def update(self, game):
        scene = game.curScene

        if(self.__health == 2):
            self.image = self.FULL
        if(self.__health == 1):
            self.image = self.HALF
        if(self.__health == 0):
            scene.removeGameObject(self)

class Stone(Block):
    def __init__(self, x, y, health = 2):
        image = Image([[Tile("["), Tile("!"), Tile("]")]])
        super().__init__(x, y, image)

    def update(self, game):
        super(Stone, self).update(game)

        self.testFalling()
        if(self.isFalling()):
            self.fall()

class Wall(Block):
    def __init__(self, x, y):
        image = Image([[Tile("="), Tile("="), Tile("=")]])
        super().__init__(x, y, image)

class Door(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "),Tile(" "),Tile(" ")]])
        super().__init__(x, y, image)
