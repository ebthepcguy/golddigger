from engine.gameObject import GameObject
from engine.image import Image
from engine.tile import Tile
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp

import level, blocks

class Character(GameObject):

    def __init__(self, x, y, image, health):
        super().__init__(x, y, image)
        self.__health = health

class Player(Character):

    xVel = 3
    yVel = 1

    fallSpeed = 1 #tiles per second

    NORAMLIMAGE = Image([[Tile("-"), Tile("O"), Tile("-")]])
    FALLINGIMAGE = Image([[Tile("~"), Tile("O"), Tile("~")]])

    def __init__(self, x, y, health = 10):
        super().__init__(x, y, self.NORAMLIMAGE, health)
        self.__game = None
        self.__fallTimer = 0
        self.falling = False

    def update(self, game):
        self.__game = game
        kb = game.keyboard

        self.testFalling()

        if(self.isFalling()):
            self.image = self.FALLINGIMAGE
            self.__fallTimer += game.deltaTime
        else:
            self.image = self.NORAMLIMAGE

        if(self.__fallTimer >= self.fallSpeed):
            self.move(0,1)
            self.__fallTimer = 0
        elif(kb.keyPressed( KeyCode.w ) and not self.isFalling()):
            self.move(0,-self.yVel)
        elif(kb.keyPressed( KeyCode.s )):
            self.move(0,self.yVel)
        elif(kb.keyPressed( KeyCode.a )):
            self.move(-self.xVel,0)
        elif(kb.keyPressed( KeyCode.d )):
            self.move(self.xVel,0)

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
            if(isinstance(gO, blocks.Dirt)):
                gO.setHealth( gO.getHealth() - 1 )


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




class Enemy(Character):

    def __init__(self, x, y, image, health):
        super().__init__(x, y, image, health)
