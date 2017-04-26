from engine.image import Image
from engine.tile import Tile
from engine.game import Game
from engine.gameObject import GameObject

class Block(GameObject):
    def __init__(self, x, y, image, collision = True):
        super().__init__(x, y, image, collision)

class Air(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "), Tile(" "), Tile(" ")]])
        super().__init__(x, y, image, False)

class Stone(Block):

    FULL = Image([[Tile("["), Tile("-"), Tile("]")]])
    HALF = Image([[Tile("["), Tile("X"), Tile("]")]])

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

class Wall(Block):
    def __init__(self, x, y):
        image = Image([[Tile("="), Tile("="), Tile("=")]])
        super().__init__(x, y, image)

class Door(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "),Tile(" "),Tile(" ")]])
        super().__init__(x, y, image)
