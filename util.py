# Create Vector object to easily keep track of locations on map
class Vector(object):
    # Each Vector has an x and y coord and cannot be changed
    def __init__(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__pair = (x,y)

    # Vectors can be added togeter by combineing thier x and y values
    def __add__(self, other):
        x = self.__x + other.__x
        y = self.__y + other.__y
        return Vector(x,y)

    # Make Vectors return true when they are both the same
    def __eq__(self, other):
        x = self.__x - other.__x
        y = self.__y - other.__y
        if x == 0 and y == 0:
            return True
        else:
            return False

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getPair(self):
        return self.__pair
