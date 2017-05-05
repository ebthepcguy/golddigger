from engine.image import Image
from engine.tile import Tile
from engine.game import Game
from engine.gameObject import GameObject
from engine.util import clamp
import level, levelEditor

class Block(GameObject):
    def __init__(self, x, y, image, collision = True):
        super().__init__(x, y, image, collision)
        self.__game = None

    def update(self, game):
        self.__game = game

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

class Gold(Block):

    FULL = Image([[Tile("["), Tile("$"), Tile("]")]])
    HALF = Image([[Tile("["), Tile("S"), Tile("]")]])

    def __init__(self, x, y, health = 2):
        image = Image([[Tile("["), Tile("$"), Tile("]")]])
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

        if(self.__health <= 0):
            scene.removeGameObject(self)
            scene.addGameObject(GoldPickup(self.x, self.y))

class Stone(Block):
    def __init__(self, x, y, health = 2):
        image = Image([[Tile("["), Tile("!"), Tile("]")]])
        super().__init__(x, y, image)
        self.__fallTimer = 0
        self.__fallDelay = 0.3
        self.__falling = False

    def update(self, game):
        super(Stone, self).update(game)
        scene = game.curScene

        if(isinstance(scene, level.Level)):
            gameArea = scene.getGameArea()

            x = clamp( self.x, gameArea.x, gameArea.width )
            y = clamp( self.y + 1, gameArea.y, gameArea.height )

            gameObjects = scene.getGameObjectsAtPos(x, y)

            self.__falling = True
            for gO in gameObjects:
                if gO.collision:
                    self.__falling = False

            if ( self.__falling ):
                self.__fallTimer += game.deltaTime
            else:
                self.__fallTimer = 0

            if ( self.__fallTimer > self.__fallDelay ):
                self.x = x
                self.y = y

class Wall(Block):
    def __init__(self, x, y):
        image = Image([[Tile("█"), Tile("█"), Tile("█")]])
        super().__init__(x, y, image)

class Door(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "),Tile(" "),Tile(" ")]])
        super().__init__(x, y, image)

    def update(self, game):
        scene = game.curScene

        if (isinstance(scene, levelEditor.LevelEditor)):
            self.image = Image([[Tile("|"), Tile("D"), Tile("|")]])
        else:
            self.image = Image([[Tile(" "), Tile(" "), Tile(" ")]])

class PlayerSpawn(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "), Tile(" "), Tile(" ")]])
        super().__init__(x, y, image)

    def update(self, game):
        scene = game.curScene

        if (isinstance(scene, levelEditor.LevelEditor)):
            self.image = Image([[Tile("|"), Tile("P"), Tile("|")]])
        else:
            self.image = Image([[Tile(" "), Tile(" "), Tile(" ")]])

class GoldPickup(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "), Tile("$"), Tile(" ")]])
        super().__init__(x, y, image)
        self.collision = False

class HealthPickup(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "), Tile("+"), Tile(" ")]])
        super().__init__(x, y, image)
        self.collision = False

class EditMarker(Block):
    def __init__(self, x, y):
        image = Image.stringToImage(" *")
        super().__init__(x, y, image)
