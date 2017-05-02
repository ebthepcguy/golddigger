from engine.gameObject import GameObject
from engine.image import Image
from engine.tile import Tile
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp
import os

import level, blocks, levelEditor


class Character(GameObject):

    def __init__(self, x, y, image, maxHealth):
        super().__init__(x, y, image)
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.__game = None
        self.__fallTimer = 0
        self.__falling = False
        self.__canDig = False
        self.__canAttack = False

    def update(self, game):
        self.__game = game

        if(self.health <= 0):
            os.system('cls')
            game.curScene.removeGameObject(self)
            print("""

             _____                        _____
            |  __ \                      |  _  |
            | |  \/ __ _ _ __ ___   ___  | | | |_   _____ _ __
            | | __ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__|
            | |_\ \ (_| | | | | | |  __/ \ \_/ /\ V /  __/ |
             \____/\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|

            """)

            print("         ------------------------------------------------------")
            print("                     You were killed by the enemy.")
            input("                    Press enter to return to the menu")


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


                if(isinstance(gO, Character)):
                    gO.health -= 1


            if(canMove):
                self.x = x
                self.y = y

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

    @property
    def maxHealth(self):
        return self.__maxHealth

    @maxHealth.setter
    def maxHealth(self, maxHealth):
        self.__maxHealth = maxHealth

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

    @property
    def canAttack(self):
        return self.__canDig

    @canAttack.setter
    def canAttack(self, canAttack):
        self.__canAttack = canAttack

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

    NORAML_IMAGE = Image([[Tile("-"), Tile("O"), Tile("-")]])
    FALLING_IMAGE = Image([[Tile("~"), Tile("O"), Tile("~")]])

    def __init__(self, x, y, maxHealth = 3):
        super().__init__(x, y, self.NORAML_IMAGE, maxHealth)
        self.canDig = True
        self.canAttack = True

    def update(self, game):
        super().update(game)
        kb = game.keyboard

        self.testFalling()

        if(self.falling):
            self.image = self.FALLING_IMAGE
            self.fallTimer += game.deltaTime
        else:
            self.image = self.NORAML_IMAGE

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

    fallSpeed = 1
    WALK_SPEED = 1
    LEFT_IMAGE = Image([[Tile("<"), Tile("<"), Tile("E")]])
    RIGHT_IMAGE = Image([[Tile("E"), Tile(">"), Tile(">")]])

    def __init__(self, x, y, maxHealth = 2):
        super().__init__(x, y, self.RIGHT_IMAGE, maxHealth)
        self.__walkTimer = 0
        self.__xVel = 3
        self.canAttack = True

    def update(self, game):
        super().update(game)
        scene = game.curScene

        if ( isinstance(scene, level.Level) ):

            # Increment time until enemy will atempt to move again
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
                # Move until collision then switch directions
                gameObjects = game.curScene.getGameObjectsAtPos(self.x + self.__xVel, self.y)
                canMove = True
                for gO in gameObjects:
                    if(gO.collision and not isinstance(gO, Player)):
                        # If we cannot move switch directions
                        canMove = False
                        self.__xVel *= -1
                        # Update Image
                        if(self.__xVel > 0):
                            self.image = self.RIGHT_IMAGE
                        elif(self.__xVel < 0):
                            self.image = self.LEFT_IMAGE
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
        scene = game.curScene

        kb = game.keyboard
        gO = ""

        if (kb.keyPressed(KeyCode.w)):
            self.move(0, -self.yVel, game)
        elif (kb.keyPressed(KeyCode.s)):
            self.move(0, self.yVel, game)
        elif (kb.keyPressed(KeyCode.a)):
            self.move(-self.xVel, 0, game)
        elif (kb.keyPressed(KeyCode.d)):
            self.move(self.xVel, 0, game)
        elif (kb.keyPressed(KeyCode.SPACEBAR)):
            gO = blocks.EditMarker(self.x, self.y)
        elif (kb.keyPressed(KeyCode.ZERO)):
            gO = blocks.Air(self.x, self.y)
        elif (kb.keyPressed(KeyCode.ONE)):
            gO = blocks.Wall(self.x, self.y)
        elif (kb.keyPressed(KeyCode.TWO)):
            gO = blocks.Dirt(self.x, self.y)
        elif (kb.keyPressed(KeyCode.THREE)):
            gO = blocks.Stone(self.x, self.y)
        elif (kb.keyPressed(KeyCode.FOUR)):
            gO = blocks.Gold(self.x, self.y)
        elif (kb.keyPressed(KeyCode.FIVE)):
            gO = blocks.GoldPickup(self.x, self.y)
        elif (kb.keyPressed(KeyCode.SIX)):
            gO = blocks.HealthPickup(self.x, self.y)
        elif (kb.keyPressed(KeyCode.SEVEN)):
            gO = blocks.PlayerSpawn(self.x, self.y)
        elif (kb.keyPressed(KeyCode.EIGHT)):
            gO = blocks.Door(self.x, self.y)
        elif (kb.keyPressed(KeyCode.NINE)):
            gO = Enemy(self.x, self.y)

        newGO = ""
        if gO:
            if ( isinstance(gO, blocks.EditMarker) ):
                if scene.hasAny(blocks.EditMarker):
                    scene.removeGameObjectsByType(blocks.EditMarker)
                    scene.addGameObject(gO, 1)
                else:
                    scene.addGameObject(gO, 1)

            else:
                if scene.hasAny(blocks.EditMarker):
                    editMarker = scene.getGameObjectsByType(blocks.EditMarker)[0]

                    if ( editMarker.x < self.x ):
                        smallX = editMarker.x
                        largeX = self.x
                    else:
                        smallX = self.x
                        largeX = editMarker.x

                    if ( editMarker.y < self.y ):
                        smallY = editMarker.y
                        largeY = self.y
                    else:
                        smallY = self.y
                        largeY = editMarker.y

                    for y in range(smallY, largeY + 1):
                        for x in range(smallX, largeX + EditCursor.xVel, EditCursor.xVel):
                            if (isinstance(gO, blocks.Air)):
                                newGO = blocks.Air(x, y)
                            elif (isinstance(gO, blocks.Wall)):
                                newGO = blocks.Wall(x, y)
                            elif (isinstance(gO, blocks.Dirt)):
                                newGO = blocks.Dirt(x, y)
                            elif (isinstance(gO, blocks.Stone)):
                                newGO = blocks.Stone(x, y)
                            elif (isinstance(gO, blocks.Gold)):
                                newGO = blocks.Gold(x, y)
                            elif (isinstance(gO, blocks.GoldPickup)):
                                newGO = blocks.GoldPickup(x, y)
                            elif (isinstance(gO, blocks.HealthPickup)):
                                newGO = blocks.HealthPickup(x, y)
                            elif (isinstance(gO, blocks.PlayerSpawn)):
                                newGO = blocks.PlayerSpawn(x, y)
                            elif (isinstance(gO, blocks.Door)):
                                newGO = blocks.Door(x, y)
                            elif (isinstance(gO, Enemy)):
                                newGO = Enemy(x, y)
                            """
                            newGO = gO
                            newGO.x = x
                            newGO.y = y
                            """
                            scene.removeGameObjectsAtPos(x, y, self)
                            scene.addGameObject(newGO)
                else:
                    scene.removeGameObjectsAtPos(self.x, self.y, self)
                    scene.addGameObject(gO)

    def move(self, x, y, game):
        scene = game.curScene

        if (isinstance(scene, levelEditor.LevelEditor)):
            gameArea = scene.getGameArea()

            x = clamp(self.x + x, gameArea.x, gameArea.width - 2)
            y = clamp(self.y + y, gameArea.y, gameArea.height)

            self.x = x
            self.y = y
