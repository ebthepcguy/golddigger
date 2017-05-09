from engine.util import Rect
import engine.image, engine.util, engine.tile, engine.util

class GameObject(object):

    def __init__(self, x, y, image = None, collision = True, destructable = False):
        self.__x = x
        self.__y = y
        self.__image = None
        self.image = image
        self.__collision = collision # If the object has collision
        self.__destructable = destructable
        self.__canPause = True

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image
        # When the image is updated update the Rect
        self.generateRect()

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect

    @property
    def collision(self):
        return self.__collision

    @collision.setter
    def collision(self, collision):
        self.__collision = collision

    @property
    def destructable(self):
        return self.__destructable

    @destructable.setter
    def destructable(self, destructable):
        self.__destructable = destructable

    @property
    def canPause(self):
        return self.__canPause

    @canPause.setter
    def canPause(self, canPause):
        self.__canPause = canPause

    def generateRect(self):

        # If the object has no image, give it a 1 by 1 Rectangle
        if(self.__image is None):
            self.__rect = Rect(1,1)
        else:
            imageTiles = self.__image.tiles
            width = 0
            height = len(imageTiles)

            # Get the maximum width of the image and set that to the width
            #   of the Rectangle
            for row in imageTiles:
                lenOfRow = len(row)
                if(lenOfRow > width):
                    width = lenOfRow

            self.__rect = engine.util.Rect(width,height)

    def update(self):
        pass
