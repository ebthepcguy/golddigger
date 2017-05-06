from engine.image import Image
from engine.tile import Tile
from engine.game import Game
from engine.gameObject import GameObject
from engine.util import clamp
import level, levelEditor, characters

class Block(GameObject):
    def __init__(self, x, y, image, collision = True):
        super().__init__(x, y, image, collision)
        self.__game = None
        self.__health = 1
        self.__canFall = False
        self.__canHurt = False
        self.__fallTimer = 0
        self.__fallDelay = 0.3
        self.__falling = False

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, game):
        self.__game = game

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if self.__health <= 0:
            self.__game.curScene.removeGameObject(self)

    @property
    def canFall(self):
        return self.__canFall

    @canFall.setter
    def canFall(self, canFall):
        self.__canFall = canFall

    @property
    def canHurt(self):
        return self.__canHurt

    @canHurt.setter
    def canHurt(self, canHurt):
        self.__canHurt = canHurt

    @property
    def falling(self):
        return self.__falling

    @falling.setter
    def falling(self, falling):
        self.__falling = falling

    def update(self, game):
        self.__game = game

        scene = game.curScene

        if( isinstance(scene, level.Level) and self.__canFall ):
            gameArea = scene.getGameArea()

            x = clamp( self.x, gameArea.x, gameArea.width )
            y = clamp( self.y + 1, gameArea.y, gameArea.height )

            gameObjects = scene.getGameObjectsAtPos(x, y)

            if len(gameObjects) == 0:
                self.__falling = True

            for gO in gameObjects:
                if gO.destructable and self.__canHurt and self.__falling and not isinstance(gO, Dirt):
                    gO.health -= 1
                    self.health -= 1
                if gO.collision:
                    self.__falling = False

            if ( self.__falling ):
                self.__fallTimer += game.deltaTime
            else:
                self.__fallTimer = 0

            if ( self.__fallTimer > self.__fallDelay ):
                self.x = x
                self.y = y

class Dirt(Block):

    FULL = Image([[Tile("▒"), Tile("▒"), Tile("▒")]])
    HALF = Image([[Tile("░"), Tile("░"), Tile("░")]])

    def __init__(self, x, y, health = 2):
        image = self.FULL
        super().__init__(x, y, image)
        self.health = health
        self.destructable = True

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if(self.__health >= 2):
            self.image = self.FULL
        if(self.__health == 1):
            self.image = self.HALF
        if(self.__health <= 0):
            self.game.curScene.removeGameObject(self)

    def update(self, game):
        super().update(game)

class Gold(Block):

    FULL = Image([[Tile("["), Tile("$"), Tile("]")]])
    HALF = Image([[Tile("("), Tile("$"), Tile(")")]])
    LITTLE = Image([[Tile("{"), Tile("$"), Tile("}")]])

    def __init__(self, x, y, health = 3):
        image = self.FULL
        super().__init__(x, y, image)
        self.health = health
        self.destructable = True

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if(self.__health >= 3):
            self.image = self.FULL
        elif(self.__health == 2):
            self.image = self.HALF
        elif(self.__health == 1):
            self.image = self.LITTLE
        elif(self.__health <= 0):
            self.game.curScene.addGameObject(GoldPickup(self.x, self.y))
            self.game.curScene.removeGameObject(self)

    def update(self, game):
        super().update(game)

class Stone(Block):
    def __init__(self, x, y, health = 2):
        image = Image([[Tile("["), Tile("#"), Tile("]")]])
        super().__init__(x, y, image)
        self.canFall = True
        self.canHurt = True
        self.health = 1

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if self.__health <= 0:
            self.game.curScene.addGameObject(Smoke(self.x, self.y), 2)
            self.game.curScene.removeGameObject(self)

    def update(self, game):
        super().update(game)

class Wall(Block):
    def __init__(self, x, y):
        image = Image([[Tile("█"), Tile("█"), Tile("█")]])
        super().__init__(x, y, image)

class Door(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "),Tile(" "),Tile(" ")]])
        super().__init__(x, y, image)

    def update(self, game):
        super().update(game)
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
        super().update(game)
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
        self.canFall = True

    def update(self, game):
        super().update(game)

class HealthPickup(Block):
    def __init__(self, x, y):
        image = Image([[Tile(" "), Tile("+"), Tile(" ")]])
        super().__init__(x, y, image)
        self.collision = False
        self.canFall = True

    def update(self, game):
        super().update(game)

class EditMarker(Block):
    def __init__(self, x, y):
        image = Image.stringToImage(" *")
        super().__init__(x, y, image)

    def update(self, game):
        super().update(game)

class Bomb(Block):

    FULL = Image([[Tile("["), Tile("?"), Tile("]")]])
    HALF = Image([[Tile("{"), Tile("!"), Tile("}")]])
    THREE = Image([[Tile("{"), Tile("3"), Tile("}")]])
    TWO = Image([[Tile("{"), Tile("2"), Tile("}")]])
    ONE = Image([[Tile("{"), Tile("1"), Tile("}")]])

    def __init__(self, x, y, health = 2):
        image = self.FULL
        super().__init__(x, y, image)
        self.health = health
        self.destructable = True
        self.canHurt = True
        self.__fullFuseTime = 3
        self.__fuseTime = self.__fullFuseTime
        self.__fuseLit = False

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if(self.__health >= 2):
            self.image = self.FULL
        elif(self.__health == 1):
            self.image = self.HALF
            self.canFall = True
        elif(self.__health <= 0):
            self.__fuseLit = True

    def update(self, game):
        super().update(game)

        if self.__fuseLit:
            self.__fuseTime -= game.deltaTime

            if self.__fuseTime >= self.__fullFuseTime * 0.66:
                self.image = self.THREE
            elif self.__fuseTime >= self.__fullFuseTime * 0.33:
                self.image = self.TWO
            elif self.__fuseTime >= 0:
                self.image = self.ONE
            else:
                self.blowUp()

    def blowUp(self):
        scene = self.game.curScene
        blockWidth = 3
        blockHeight = 1
        """
        for x in range(self.x - (blockWidth*2), self.x + (blockWidth*3), blockWidth):
            for y in range(self.y - (blockHeight*2), self.y + (blockHeight*3), blockHeight):
                if not ( x == self.x and y == self.y ):
                    gameObjects = scene.getGameObjectsAtPos(x, y)
                    for gO in gameObjects:
                        if gO.destructable:
                            if ( abs(self.x - x) <= blockWidth and abs(self.y - y) <= blockHeight ):
                                gO.health -= 2
                            else:
                                gO.health -= 1

                smoke = Smoke(x, y)
                scene.addGameObject(smoke ,2)
        """
        self.blastDiagonal(1,1)
        self.blastDiagonal(-1,1)
        self.blastDiagonal(1,-1)
        self.blastDiagonal(-1,-1)
        self.blastAdjacentX(-1)
        self.blastAdjacentX(1)
        self.blastAdjacentY(1)
        self.blastAdjacentY(-1)

        self.addSmoke(self.x, self.y)

        scene.removeGameObject(self)

    def blastAdjacentX(self, signX):
        scene = self.game.curScene
        x = self.x
        y = self.y
        blockWidth = 3
        blockHeight = 1

        gameObjects = scene.getGameObjectsAtPos(x + (blockWidth * signX), y)
        wall = False
        for gO in gameObjects:
            self.doDamage(gO)
            if isinstance(gO, Wall):
                wall = True
        self.addSmoke(x + (blockWidth * signX), y)
        if not wall:
            gameObjects = scene.getGameObjectsAtPos(x + (blockWidth * 2 * signX), y)
            for gO in gameObjects:
                self.doDamage(gO)
            self.addSmoke(x + (blockWidth * 2 * signX), y)

    def blastAdjacentY(self, signY):
        scene = self.game.curScene
        x = self.x
        y = self.y
        blockWidth = 3
        blockHeight = 1

        gameObjects = scene.getGameObjectsAtPos(x, y + (blockHeight * signY))
        wall = False
        for gO in gameObjects:
            self.doDamage(gO)
            if isinstance(gO, Wall):
                wall = True
        self.addSmoke(x, y + (blockHeight * signY))
        if not wall:
            gameObjects = scene.getGameObjectsAtPos(x, y + (blockHeight * 2 * signY))
            for gO in gameObjects:
                self.doDamage(gO)
            self.addSmoke(x, y + (blockHeight * 2 * signY))


    def blastDiagonal(self, signX, signY):
        scene = self.game.curScene
        x = self.x
        y = self.y
        blockWidth = 3
        blockHeight = 1

        gameObjects = scene.getGameObjectsAtPos(x + (blockWidth * signX), y + (blockHeight * signY))
        wall = False
        for gO in gameObjects:
            self.doDamage(gO)
            if isinstance(gO, Wall):
                wall = True
        self.addSmoke(x + (blockWidth * signX), y + (blockHeight * signY))
        if not wall:
            gameObjects = scene.getGameObjectsAtPos(x + (blockWidth * 2 * signX), y + (blockHeight * signY))
            for gO in gameObjects:
                self.doDamage(gO)
            self.addSmoke(x + (blockWidth * 2 * signX), y + (blockHeight * signY))
            gameObjects = scene.getGameObjectsAtPos(x + (blockWidth * 2 * signX), y + (blockHeight * 2 * signY))
            for gO in gameObjects:
                self.doDamage(gO)
            self.addSmoke(x + (blockWidth * 2 * signX), y + (blockHeight * 2 * signY))
            gameObjects = scene.getGameObjectsAtPos(x + (blockWidth * signX), y + (blockHeight * 2 * signY))
            for gO in gameObjects:
                self.doDamage(gO)
            self.addSmoke(x + (blockWidth * signX), y + (blockHeight * 2 * signY))

    def doDamage(self, gO):
        blockWidth = 3
        blockHeight = 1
        if gO.destructable:
            if ( abs(self.x - gO.x) <= blockWidth and abs(self.y - gO.y) <= blockHeight ):
                gO.health -= 2
            else:
                gO.health -= 1

    def addSmoke(self, x, y):
        scene = self.game.curScene
        smoke = Smoke(x , y)
        scene.addGameObject(smoke ,3)

class Smoke(Block):

    def __init__(self, x, y, health = 2):
        image = Image.stringToImage("▓▓▓")
        super().__init__(x, y, image)
        self.health = 2

    def update(self, game):
        import random
        super().update(game)
        r = random.randint(1, 2)
        if r == 2:
            self.health -= 1

        scene = self.game.curScene

        gameObjects = scene.getGameObjectsAtPos(self.x, self.y)
        smokeCount = 0
        for gO in gameObjects:
            if isinstance(gO, Smoke):
                smokeCount =+ 1

        if smokeCount > 1:
            scene.removeGameObject(self)
