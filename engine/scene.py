import engine.gameObject, engine.screenBuffer, engine.game
from engine.popup import Popup

class Scene(object):

    def __init__(self):
        self.__gameObjects = [[] for _ in range(10)]
        self.__paused = False
        self.__originalGameObjects = None

    @property
    def gameObjects(self):
        return self.__gameObjects

    @gameObjects.setter
    def gameObjects(self, gameObjects):
        self.__gameObjects = gameObjects

    @property
    def paused(self):
        return self.__paused

    @paused.setter
    def paused(self, paused):
        self.__paused = paused

    @property
    def originalGos(self):
        return self.__originalGos

    @originalGos.setter
    def originalGos(self, originalGos):
        self.__originalGos = originalGos

    def load(self):
        pass

    def update(self, game):
        pass

    def updateGameObjects(self):
        for layer in self.__gameObjects:
            for gO in layer:
                if not self.__paused:
                    gO.update(self.__game)
                elif isinstance(gO, Popup):
                    if gO.focusedOn == True:
                        gO.update(self.__game)

    def draw(self):

        screenBuffer = self.__game.screenBuffer

        for layer in self.__gameObjects:
            for gO in layer:
                image = gO.image
                tileX = gO.x
                tileY = gO.y

                for row in image.tiles:
                    for tile in row:
                        screenBuffer.addTile(tile, tileX, tileY)
                        tileX += 1
                    tileX = gO.x
                    tileY += 1

        screenBuffer.draw()

    def addGameObject(self, gO, layer = 0):
        if(layer in range(0,10)):
            self.__gameObjects[layer].append(gO)

    def removeGameObject(self, gO):
        for layer in self.__gameObjects:
            if(gO in layer):
                layer.remove(gO)

    def getGameObjectsByType(self, type):
        gOWithType = []

        for layer in self.__gameObjects:
            for gO in layer:
                if(isinstance(gO, type)):
                    gOWithType.append(gO)

        return gOWithType

    def removeGameObjectsByType(self, type):
        for layer in self.__gameObjects:
            for gO in layer:
                if(isinstance(gO, type)):
                    self.removeGameObject(gO)

    def getGameObjectsAtPos(self,x,y):

        gOAtPos = []

        for layer in self.__gameObjects:
            for gO in layer:

                gOX = gO.x
                gOY = gO.y
                gOWidth = gO.rect.width
                gOHeight = gO.rect.height

                # Check if the x and y are within the Rectangle of the object
                if(x >= gOX and x < gOWidth + gOX \
                    and y >= gOY and y < gOHeight + gOY):
                    gOAtPos.append(gO)

        return gOAtPos

    def removeGameObjectsAtPos(self,x,y, exclude = None):
        gOs = self.getGameObjectsAtPos(x, y)
        for gO in gOs:
            if gO != exclude:
                self.removeGameObject(gO)

    def hasAny(self, type):
        out = False
        for layer in self.__gameObjects:
            for gO in layer:
                if(isinstance(gO, type)):
                    out = True
        return out

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, game):
        self.__game = game

    def len(self):
        num = 0
        for layer in self.__gameObjects:
            num += len(layer)

        return num
