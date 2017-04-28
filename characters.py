from engine.gameObject import GameObject
from engine.image import Image
from engine.tile import Tile
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp

import level, blocks, levelEditor

class Character(GameObject):

    def __init__(self, x, y, image, health):
        super().__init__(x, y, image)
        self.__health = health
        self.__game = None
        self.__fallTimer = 0
        self.__falling = False
        self.__canDig = False

    def update(self, game):
        self.__game = game

    def move(self, x, y):
        scene = self.__game.curScene

        if(isinstance(scene, level.Level)):
            gameArea = scene.getGameArea()

            x = clamp( self.x + x, gameArea.x, gameArea.width )
            y = clamp( self.y + y, gameArea.y, gameArea.height )


            gameObjects = scene.getGameObjectsAtPos(x, y)

            canMove = True

            for gO in gameObjects:
                if(gO.collision):
                    canMove = False
                if(self.canDig):
                    if(isinstance(gO, blocks.Dirt)):
                        gO.setHealth( gO.getHealth() - 1 )


            if(canMove):
                self.x = x
                self.y = y

    @property
    def falling(self):
        return self.__falling

    @falling.setter
    def falling(self, falling):
        self.__falling = falling

    @property
    def fallTimer(self):
        return self.__fallTimer

    @fallTimer.setter
    def fallTimer(self, fallTimer):
        self.__fallTimer = fallTimer

    @property
    def canDig(self):
        return self.__canDig

    @canDig.setter
    def canDig(self, canDig):
        self.__canDig = canDig

    def testFalling(self):
        scene = self.__game.curScene
        gameObjects = scene.getGameObjectsAtPos(self.x, self.y + 1)
        isFalling = True
        for gO in gameObjects:
            if(gO.collision):
                isFalling = False

        self.falling = isFalling



class Player(Character):

    xVel = 3
    yVel = 1

    fallSpeed = 1 #tiles per second

    NORAMLIMAGE = Image([[Tile("-"), Tile("O"), Tile("-")]])
    FALLINGIMAGE = Image([[Tile("~"), Tile("O"), Tile("~")]])

    def __init__(self, x, y, health = 10):
        super().__init__(x, y, self.NORAMLIMAGE, health)
        self.canDig = True

    def update(self, game):
        super().update(game)
        kb = game.keyboard

        self.testFalling()

        if(self.falling):
            self.image = self.FALLINGIMAGE
            self.fallTimer += game.deltaTime
        else:
            self.image = self.NORAMLIMAGE

        if(self.fallTimer >= self.fallSpeed):
            self.move(0,1)
            self.fallTimer = 0
        elif(kb.keyPressed( KeyCode.w ) and not self.falling):
            self.move(0,-self.yVel)
        elif(kb.keyPressed( KeyCode.s )):
            self.move(0,self.yVel)
        elif(kb.keyPressed( KeyCode.a )):
            self.move(-self.xVel,0)
        elif(kb.keyPressed( KeyCode.d )):
            self.move(self.xVel,0)




class Enemy(Character):

    WALK_SPEED = 1
    fallSpeed = 1
    NORAMLIMAGE = Image([[Tile("<"), Tile("E"), Tile(">")]])
    def __init__(self, x, y, health = 2):
        super().__init__(x, y, self.NORAMLIMAGE, health)
        self.__walkTimer = 0
        self.__xVel = 3

    def update(self, game):
        super().update(game)

        self.__walkTimer += game.deltaTime
        self.testFalling()

        if(self.falling):
            self.fallTimer += game.deltaTime

        if(self.fallTimer >= self.fallSpeed):
            self.move(0,1)
            self.fallTimer = 0
        elif(self.__walkTimer >= self.WALK_SPEED):
            self.__walkTimer = 0

            # Movement AI
            # Move untill collision then switch directions
            gameObjects = game.curScene.getGameObjectsAtPos(self.x + self.__xVel, self.y)
            canMove = True
            for gO in gameObjects:
                if(gO.collision):
                    canMove = False
                    self.__xVel *= -1

            if(canMove):
                self.move(self.__xVel , 0)



class EditCursor(Character):

    xVel = 3
    yVel = 1

    def __init__(self, x, y, health = 10):
        image = Image.stringToImage("{")
        super().__init__(x, y, image, health)

    def update(self, game):
        super().update(game)
        scene = self.getGame().curScene

        kb = game.keyboard
        gO = ""

        if (kb.keyPressed(KeyCode.w)):
            self.move(0, -self.yVel)
        elif (kb.keyPressed(KeyCode.s)):
            self.move(0, self.yVel)
        elif (kb.keyPressed(KeyCode.a)):
            self.move(-self.xVel, 0)
        elif (kb.keyPressed(KeyCode.d)):
            self.move(self.xVel, 0)
        elif (kb.keyPressed(KeyCode.ZERO)):
            scene.removeGameObjectsAtPos(self.x, self.y, self)
        elif (kb.keyPressed(KeyCode.ONE)):
            gO = blocks.Dirt(self.x, self.y)
        elif (kb.keyPressed(KeyCode.TWO)):
            gO = blocks.Air(self.x, self.y)
        elif (kb.keyPressed(KeyCode.THREE)):
            gO = blocks.Stone(self.x, self.y)
        elif (kb.keyPressed(KeyCode.FOUR)):
            gO = blocks.Wall(self.x, self.y)
        elif (kb.keyPressed(KeyCode.FIVE)):
            gO = Enemy(self.x, self.y)

        if gO:
            scene.removeGameObjectsAtPos(self.x, self.y, self)
            scene.addGameObject(gO)

    def move(self, x, y):
        scene = self.getGame().curScene

        if (isinstance(scene, levelEditor.LevelEditor)):
            gameArea = scene.getGameArea()

            x = clamp(self.x + x, gameArea.x, gameArea.width)
            y = clamp(self.y + y, gameArea.y, gameArea.height)

            self.x = x
            self.y = y
