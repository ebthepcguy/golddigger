from engine.tile import Tile
import os

class ScreenBuffer(object):

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__buffer = [[ Tile(" ") for _ in range(width)] for _ in range(height)]

    def clear(self):
        self.__buffer = [[ Tile( " " ) for _ in range(self.__width)] for _ in range(self.__height)]

    def addTile(self,tile, x, y):
        if( x >= 0 and x < self.__width \
        and y >= 0 and y < self.__height ):
            self.__buffer[y][x] = tile

    def draw(self):
        printString = ""

        for row in self.__buffer:
            for tile in row:
                printString += tile.char
            printString += "\n"

        # Stops extra newline from pushing screen up by one
        printString = printString[:len(printString) - 2]

        # Clears the screen WINDOWS ONLY
        os.system("CLS")
        print(printString, end="")

        self.clear()
