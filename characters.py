from engine.game import Game
from engine.gameObject import GameObject
from engine.image import Image
from engine.tile import Tile
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp
from debugDisplay import DebugDisplay

import level, blocks, levelEditor, copy, menu, time

class Character(GameObject):

    def __init__(self, x, y, image, maxHealth = 3):
        super().__init__(x, y, image)
        self.__maxHealth = maxHealth
        self.__health = self.__maxHealth
        self.__canAttack = False
        self.__airTime = 1
        self.__timeJumped = 0
        self.__falling = False

    @property
    def maxHealth(self):
        return self.__maxHealth

    @maxHealth.setter
    def maxHealth(self, maxHealth):
        self.__maxHealth = maxHealth

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

    @property
    def falling(self):
        return self.__falling

    @falling.setter
    def falling(self, falling):
        self.__falling = falling

    @property
    def timeJumped(self):
        return self.__timeJumped

    @timeJumped.setter
    def timeJumped(self, timeJumped):
        self.__timeJumped = timeJumped

    @property
    def airTime(self):
        return self.__airTime

    @airTime.setter
    def airTime(self, airTime):
        self.__airTime = airTime

    @property
    def canAttack(self):
        return self.__canAttack

    @canAttack.setter
    def canAttack(self, canAttack):
        self.__canAttack = canAttack

    def update(self):
        pass

    def move(self, x, y):
        pass

    def jump(self):
        if not self.falling:
            scene = Game.curGame.curScene

            gameObjects = scene.getGameObjectsAtPos(self.x, self.y + 1)
            onSolidGround = False
            for gO in gameObjects:
                if(gO.collision):
                    onSolidGround = True

            gameObjects = scene.getGameObjectsAtPos(self.x, self.y - 1)
            canJump = True
            for gO in gameObjects:
                if(gO.collision):
                    canJump = False

            y = clamp(self.y - 1, scene.gameArea.y, scene.gameArea.height)

            if onSolidGround and canJump:
                self.y = y
                self.timeJumped = time.time()

    def updateFalling(self):
        scene = Game.curGame.curScene

        gameObjects = scene.getGameObjectsAtPos(self.x, self.y + 1)
        onSolidGround = False
        for gO in gameObjects:
            if gO.collision:
                onSolidGround = True
                self.falling = False

        if not onSolidGround:
            if ( time.time() > self.airTime + self.timeJumped ):
                self.falling = True

        if self.falling:
            self.move(0,1)

    def tryToPush(self, block):
        blockPushed = False
        if block.pushable:
            scene = Game.curGame.curScene
            gameAria = Game.curGame.curScene.gameArea

            xDir = None

            if (self.x < block.x and self.y == block.y):
                xDir = 1
            elif (self.x > block.x and self.y == block.y):
                xDir = -1

            if(xDir):
                gameObjects = scene.getGameObjectsAtPos(block.x + (xDir*3), block.y)
                if len(gameObjects) == 0:
                    block.x += xDir*3
                    self.x += xDir*3
                    blockPushed = True

        return blockPushed

class Player(Character):

    xVel = 3
    yVel = 1

    NORAML_IMAGE = Image([[Tile("-"), Tile("O"), Tile("-")]])
    FALLING_IMAGE = Image([[Tile("~"), Tile("O"), Tile("~")]])

    def __init__(self, x, y, maxHealth = 3):
        super().__init__(x, y, self.NORAML_IMAGE, maxHealth)
        self.__health = maxHealth
        self.__gold = 0
        self.__level = 1
        self.__falling = False
        self.canAttack = True
        self.destructable = True

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if self.health <= 0:
            self.lose()

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

    @property
    def falling(self):
        return self.__falling

    @falling.setter
    def falling(self, falling):
        self.__falling = falling

        if self.falling:
            self.image = self.FALLING_IMAGE
        else:
            self.image = self.NORAML_IMAGE

    def update(self):
        super().update()

        kb = Game.curGame.keyboard

        self.updateFalling()

        if(kb.keyPressed( KeyCode.SPACEBAR )):
            self.jump()
        elif(kb.keyPressed( KeyCode.w )):
            self.hitAboveBlock()
            self.jump()
        elif(kb.keyPressed( KeyCode.s )):
            self.move(0,self.yVel)
        elif(kb.keyPressed( KeyCode.a )):
            self.move(-self.xVel,0)
        elif(kb.keyPressed( KeyCode.d )):
            self.move(self.xVel,0)
        elif(kb.keyPressed( KeyCode.h )):
            self.health += 1

    def hitAboveBlock(self):
        scene = Game.curGame.curScene

        gameObjects = scene.getGameObjectsAtPos(self.x, self.y - 1)
        for gO in gameObjects:
            if gO.destructable:
                gO.health -= 1

    def move(self, x, y):
        super().move(x, y)
        scene = Game.curGame.curScene

        gameArea = scene.gameArea

        x = clamp( self.x + x, gameArea.x, gameArea.width + 1 )
        y = clamp( self.y + y, gameArea.y, gameArea.height + 1)

        canMove = True
        gameObjects = scene.getGameObjectsAtPos(x, y)
        for gO in gameObjects:
            if(gO.collision):
                canMove = False

            if gO.destructable:
                gO.health -= 1

            if(isinstance(gO, blocks.Dirt)):
                pass
            elif(isinstance(gO, blocks.Stone)):
                self.tryToPush(gO)
            elif(isinstance(gO, blocks.Gold)):
                pass
            elif(isinstance(gO, blocks.Wall)):
                pass
            elif(isinstance(gO, blocks.Door)):
                if ( self.level == level.Level.MAX_LEVEL ):
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
                pass
            elif(isinstance(gO, blocks.Bomb)):
                self.tryToPush(gO)

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
            l.generateMap()

        l.player = self

        s.close()

        Game.curGame.loadScene(l)

    def win(self):
        import os
        os.system('cls')
        print("""

        __   __           __        ___
        \ \ / /__  _   _  \ \      / (_)_ __
         \ V / _ \| | | |  \ \ /\ / /| | '_ \\
          | | (_) | |_| |   \ V  V / | | | | |
          |_|\___/ \__,_|    \_/\_/  |_|_| |_|

        """)

        print("         ------------------------------------------------------")
        print(" Final Gold: " + str(self.gold))
        input(" Press enter to quit to main menu")

        Game.curGame.curScene.removeGameObjectsByType(DebugDisplay)
        Game.curGame.loadScene(menu.MainMenu())

        Game.curGame.curScene.removeGameObject(self)

    def lose(self):
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

        Game.curGame.curScene.removeGameObjectsByType(DebugDisplay)
        Game.curGame.loadScene(menu.MainMenu())

        Game.curGame.curScene.removeGameObject(self)

class Enemy(Character):

    fallSpeed = 1
    WALK_SPEED = 1

    def __init__(self, x, y, maxHealth = 2):
        self.__leftImage = Image([[Tile("<"), Tile("<"), Tile("ö")]])
        self.__rightImage = Image([[Tile("ö"), Tile(">"), Tile(">")]])
        super().__init__(x, y, self.__rightImage, maxHealth)
        self.__health = maxHealth
        self.__walkTimer = 0
        self.__xVel = 3
        self.__canDig = False
        self.__canPush = False
        self.canAttack = True
        self.destructable = True

    def __str__(self):
        out = "Normal Enemy"
        if self.canDig:
            out = "Digging Enemy"
        elif self.canPush:
            out = "Pushing Enemy"
        out += "   Health: " + "(+│-)" + str(self.health) + "/" + str(self.maxHealth)
        out += "   (*)Change Type   (/)Change Direction"
        return out

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if self.health <= 0:
            Game.curGame.curScene.removeGameObject(self)

    @property
    def canDig(self):
        return self.__canDig

    @canDig.setter
    def canDig(self, canDig):
        self.__canDig = canDig

        if self.canDig:
            self.canPush = False

        self.updateImage()

    @property
    def canPush(self):
        return self.__canPush

    @canPush.setter
    def canPush(self, canPush):
        self.__canPush = canPush

        if self.canPush:
            self.canDig = False

        self.updateImage()

    def updateImage(self):
        if self.canPush:
            self.__leftImage = Image([[Tile("╠"), Tile("═"), Tile("Ö")]])
            self.__rightImage = Image([[Tile("Ö"), Tile("═"), Tile("╣")]])
        elif self.canDig:
            self.__leftImage = Image([[Tile("«"), Tile("«"), Tile("ö")]])
            self.__rightImage = Image([[Tile("ö"), Tile("»"), Tile("»")]])
        else:
            self.__leftImage = Image([[Tile("<"), Tile("<"), Tile("ö")]])
            self.__rightImage = Image([[Tile("ö"), Tile(">"), Tile(">")]])
        if(self.__xVel > 0):
            self.image = self.__rightImage
        elif(self.__xVel < 0):
            self.image = self.__leftImage

    def update(self, ):
        super().update()
        scene = Game.curGame.curScene

        if ( isinstance(scene, level.Level) ):

            self.updateFalling()

            # Increment time until enemy will atempt to move again
            self.__walkTimer += Game.curGame.deltaTime

            if(self.__walkTimer >= self.WALK_SPEED):
                self.__walkTimer = 0
                self.move(self.__xVel , 0)

    def move(self, x, y):
        super().move(x, y)
        scene = Game.curGame.curScene
        gameArea = scene.gameArea

        x = clamp( self.x + x, gameArea.x, gameArea.width)
        y = clamp( self.y + y, gameArea.y, gameArea.height)

        canMove = True
        gameObjects = scene.getGameObjectsAtPos(x, y)
        for gO in gameObjects:
            if(gO.collision):
                canMove = False

            if gO.destructable and self.canDig and not isinstance(gO, Enemy):
                gO.health -= 1

            if(isinstance(gO, blocks.Dirt)):
                self.reverseDir()
            elif(isinstance(gO, blocks.Stone)):
                if self.canPush and not self.tryToPush(gO):
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
            elif(isinstance(gO, blocks.Bomb)):
                if self.canPush and not self.tryToPush(gO):
                    self.reverseDir()

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

    def update(self):
        super().update()

        kb = Game.curGame.keyboard

        if (kb.keyPressed(KeyCode.w)):
            self.move(0, -self.yVel)
        elif (kb.keyPressed(KeyCode.s)):
            self.move(0, self.yVel)
        elif (kb.keyPressed(KeyCode.a)):
            self.move(-self.xVel, 0)
        elif (kb.keyPressed(KeyCode.d)):
            self.move(self.xVel, 0)

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
        elif (kb.keyPressed(KeyCode.PERIOD)):
            gO = blocks.Bomb(self.x, self.y)
        else:
            placeBlock = False

        if(placeBlock):
            self.placeBlock(gO)

        gameObjects = Game.curGame.curScene.getGameObjectsAtPos(self.x, self.y)

        for gO in gameObjects:

            if gO.destructable:
                if isinstance(gO, Enemy):
                    if (kb.keyPressed(KeyCode.PLUS)):
                        gO.maxHealth += 1
                        gO.health = clamp(gO.health + 1, 1, gO.maxHealth + 1)
                    elif (kb.keyPressed(KeyCode.MINUS)):
                        gO.maxHealth = clamp(gO.maxHealth - 1, 1, gO.maxHealth + 1)
                        gO.health = clamp(gO.health - 1, 1, gO.maxHealth + 1)
                else:
                    if (kb.keyPressed(KeyCode.PLUS)):
                        gO.health = clamp(gO.health + 1, 1, gO.maxHealth + 1)
                    elif (kb.keyPressed(KeyCode.MINUS)):
                        gO.health = clamp(gO.health - 1, 1, gO.maxHealth + 1)

            if isinstance(gO, Enemy):
                if (kb.keyPressed(KeyCode.TIMES)):
                    if not gO.canDig and not gO.canPush:
                        gO.canPush = True
                    elif gO.canPush:
                        gO.canDig = True
                    elif gO.canDig:
                        gO.canDig = False
                        gO.canPush = False
                elif (kb.keyPressed(KeyCode.DIVIDE)):
                    gO.reverseDir()
            elif isinstance(gO, blocks.Bomb):
                if (kb.keyPressed(KeyCode.TIMES)):
                    gO.fullFuseTime = clamp(gO.fullFuseTime + 1, 1, 11)
                elif (kb.keyPressed(KeyCode.DIVIDE)):
                    gO.fullFuseTime = clamp(gO.fullFuseTime - 1, 1, 11)
                elif (kb.keyPressed(KeyCode.ENTER)):
                    gO.health = 0

    def placeBlock(self, gO):
        scene = Game.curGame.curScene
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

    def move(self, x, y):
        scene = Game.curGame.curScene

        blockWidth = 3
        blockHeight = 1

        if (isinstance(scene, levelEditor.LevelEditor)):
            gameArea = scene.gameArea

            x = clamp(self.x + x, gameArea.x, gameArea.width + 1)
            y = clamp(self.y + y, gameArea.y, gameArea.height + 1)

            self.x = x
            self.y = y
