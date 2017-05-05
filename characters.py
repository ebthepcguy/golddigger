
from engine.gameObject import GameObject
from engine.image import Image
from engine.tile import Tile
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp
from debugDisplay import DebugDisplay

import level, blocks, levelEditor, copy, menu

class Character(GameObject):

    def __init__(self, x, y, image, maxHealth):
        super().__init__(x, y, image)
        self.__maxHealth = maxHealth
        self.__health = self.__maxHealth
        self.__game = None
        self.__fallTimer = 0
        self.__falling = False
        self.__canAttack = False

    def update(self, game):
        self.__game = game

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
    def canAttack(self):
        return self.__canDig

    @canAttack.setter
    def canAttack(self, canAttack):
        self.__canAttack = canAttack

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, game):
        self.__game = game

    def move(self, x, y):
        pass

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
        self.__gold = 0
        self.__level = 1
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

        # TODO: CHANGE
        if(self.health <= 0):
            import os
            os.system('cls')
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
            input(" Press enter to quit to main menu")

            game.curScene.removeGameObjectsByType(DebugDisplay)
            game.loadScene(menu.MainMenu())

            game.curScene.removeGameObject(self)

    @property
    def gold(self):
        return self.__gold

    @gold.setter
    def gold(self, gold):
        self.__gold = gold

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        self.__level = level

    def move(self, x, y):
        super().move(x, y)
        scene = self.game.curScene

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
            elif(isinstance(gO, blocks.Stone)):
                pass
            elif(isinstance(gO, blocks.Gold)):
                gO.setHealth( gO.getHealth() - 1 )
            elif(isinstance(gO, blocks.Wall)):
                pass
            elif(isinstance(gO, blocks.Door)):
                if ( self.level == 5 ):
                    self.win()
                else:
                    self.goToNextLevel()
            elif(isinstance(gO, blocks.GoldPickup)):
                scene.removeGameObject(gO)
                self.gold +=1
            elif(isinstance(gO, blocks.HealthPickup)):
                scene.removeGameObject(gO)
                self.health += 1
            elif(isinstance(gO, Enemy)):
                gO.health -= 1

        if(canMove):
            self.x = x
            self.y = y

    def goToNextLevel(self):
        import pickle, shelve, menu
        s = shelve.open(menu.Menu.LEVEL_FILE)

        self.level += 1

        try:
            data = s["level_0" + str(self.__level)]
            l = level.Level()
            l.gameObjects = data
        except:
            l = level.Level()
            l.generate()

        l.player = self

        s.close()

        self.game.loadScene(l)

    def win(self):
        pass

class Enemy(Character):

    fallSpeed = 1
    WALK_SPEED = 1

    def __init__(self, x, y, maxHealth = 2):
        self.__leftImage = Image([[Tile("<"), Tile("<"), Tile("ö")]])
        self.__rightImage = Image([[Tile("ö"), Tile(">"), Tile(">")]])
        super().__init__(x, y, self.__rightImage, maxHealth)
        self.__walkTimer = 0
        self.__xVel = 3
        self.__canDig = False
        self.canAttack = True

    @property
    def canDig(self):
        return self.__canDig

    @canDig.setter
    def canDig(self, canDig):
        if canDig:
            self.__leftImage = Image([[Tile("«"), Tile("«"), Tile("Ö")]])
            self.__rightImage = Image([[Tile("Ö"), Tile("»"), Tile("»")]])
        else:
            self.__leftImage = Image([[Tile("<"), Tile("<"), Tile("ö")]])
            self.__rightImage = Image([[Tile("ö"), Tile(">"), Tile(">")]])
        if(self.__xVel > 0):
            self.image = self.__rightImage
        elif(self.__xVel < 0):
            self.image = self.__leftImage
        self.__canDig = canDig

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
                self.move(self.__xVel , 0)

        if self.health <= 0:
            scene.removeGameObject(self)

    def move(self, x, y):
        super().move(x, y)
        scene = self.game.curScene

        gameArea = scene.getGameArea()

        x = clamp( self.x + x, gameArea.x, gameArea.width )
        y = clamp( self.y + y, gameArea.y, gameArea.height )

        gameObjects = scene.getGameObjectsAtPos(x, y)

        canMove = True

        for gO in gameObjects:
            if(gO.collision):
                canMove = False

            if(isinstance(gO, blocks.Dirt)):
                if(self.canDig):
                    gO.setHealth( gO.getHealth() - 1 )
                self.reverseDir()
            elif(isinstance(gO, blocks.Stone)):
                self.reverseDir()
            elif(isinstance(gO, blocks.Gold)):
                self.reverseDir()
            elif(isinstance(gO, blocks.Wall)):
                self.reverseDir()
            elif(isinstance(gO, blocks.Door)):
                pass
            elif(isinstance(gO, blocks.GoldPickup)):
                pass
            elif(isinstance(gO, blocks.HealthPickup)):
                pass
            elif(isinstance(gO, Enemy)):
                self.reverseDir()
            elif(isinstance(gO, Player)):
                gO.health -= 1

        if(canMove):
            self.x = x
            self.y = y

    def reverseDir(self):
        self.__xVel *= -1
        if(self.__xVel > 0):
            self.image = self.__rightImage
        elif(self.__xVel < 0):
            self.image = self.__leftImage


class EditCursor(Character):

    xVel = 3
    yVel = 1

    def __init__(self, x, y, health = 10):
        image = Image.stringToImage("{")
        super().__init__(x, y, image, health)

    def update(self, game):
        super().update(game)

        kb = game.keyboard

        if (kb.keyPressed(KeyCode.w)):
            self.move(0, -self.yVel, game)
        elif (kb.keyPressed(KeyCode.s)):
            self.move(0, self.yVel, game)
        elif (kb.keyPressed(KeyCode.a)):
            self.move(-self.xVel, 0, game)
        elif (kb.keyPressed(KeyCode.d)):
            self.move(self.xVel, 0, game)

        placeBlock = True

        if (kb.keyPressed(KeyCode.SPACEBAR)):
            gO = blocks.EditMarker(self.x, self.y)
        elif (kb.keyPressed(KeyCode.ZERO)):
            gO = None
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
        else:
            placeBlock = False

        if(placeBlock):
            self.placeBlock(gO)

        gameObjects = game.curScene.getGameObjectsAtPos(self.x, self.y)

        for gO in gameObjects:
            if isinstance(gO, Enemy):
                if (kb.keyPressed(KeyCode.PLUS)):
                    gO.health += 1
                elif (kb.keyPressed(KeyCode.MINUS)):
                    gO.health = clamp(gO.health - 1, 1, 10)
                elif (kb.keyPressed(KeyCode.TIMES)):
                    if gO.canDig:
                        gO.canDig = False
                    else:
                        gO.canDig = True
                elif (kb.keyPressed(KeyCode.DIVIDE)):
                    gO.reverseDir()

    def placeBlock(self, gO):
        scene = self.game.curScene
        #Placing a new marker
        if ( isinstance(gO, blocks.EditMarker) ):
            if scene.hasAny(blocks.EditMarker):
                scene.removeGameObjectsByType(blocks.EditMarker)
                scene.addGameObject(gO, 1)
            else:
                scene.addGameObject(gO, 1)
        #Placing objects between marker
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

                        newGO = copy.copy(gO)

                        scene.removeGameObjectsAtPos(x, y, self)
                        if(gO):
                            newGO.x = x
                            newGO.y = y
                            scene.addGameObject(newGO)

            # Placing one object
            else:
                scene.removeGameObjectsAtPos(self.x, self.y, self)
                if(gO):
                    scene.addGameObject(gO)

    def move(self, x, y, game):
        scene = game.curScene

        if (isinstance(scene, levelEditor.LevelEditor)):
            gameArea = scene.getGameArea()

            x = clamp(self.x + x, gameArea.x, gameArea.width - 2)
            y = clamp(self.y + y, gameArea.y, gameArea.height)

            self.x = x
            self.y = y
