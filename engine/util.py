
class Rect (object):

        def __init__(self, width, height, x = 0, y = 0):
            self.__width = width
            self.__height = height
            self.__x = x
            self.__y = y

        @property
        def width(self):
            return self.__width

        @property
        def height(self):
            return self.__height

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

def clamp(val, min, max):
    # Non inclusive max
    if(val >= max):
        val = max - 1
    elif(val <= min):
        val = min

    return val
