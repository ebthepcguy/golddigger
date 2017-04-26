
class Tile(object):

    def __init__(self, char = " "):
        self.__char = char

    @property
    def char(self):
        return self.__char

    @char.setter
    def char(self, char):
        if(len(char) == 1):
            self.__char = char
        else:
            raise Exception("Tile char must have lenght of 1")
