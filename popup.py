from engine.game import Game
from engine.gameObject import GameObject
from engine.keyboard import Keyboard, KeyCode
from engine.image import Image
from engine.util import clamp

class Popup(GameObject):

    def __init__(self, *options):

        self.__options = options
        self.__activeOption = 0
        self.__focusedOn = True

        image = self.generateCurrentImage()
        image = Image.stringToImage(image)

        super().__init__(18, 15, image)

        self.canPause = False

    @property
    def activeOption(self):
        return self.__activeOption

    @activeOption.setter
    def activeOption(self, activeOption):
        self.__activeOption = activeOption

    @property
    def focusedOn(self):
        return self.__focusedOn

    @focusedOn.setter
    def focusedOn(self, focusedOn):
        self.__focusedOn = focusedOn

    def update(self):
        kb = Game.curGame.keyboard

        if (kb.keyPressed(KeyCode.w)):
            self.__activeOption -= 1
        elif (kb.keyPressed(KeyCode.s)):
            self.__activeOption += 1

        self.__activeOption = clamp( self.__activeOption, 0, len(self.__options))

        image = self.generateCurrentImage()
        self.image = Image.stringToImage(image)

    def generateCurrentImage(self):
        length = 20
        image = " " * length + "\n"
        activeOption = 0
        for option in self.__options:
            if activeOption == self.__activeOption:
                i = " > "
            else:
                i = "   "
            i += option
            num = length - len(i)
            image += i + (" " * num) + "\n"
            activeOption += 1
        image += " " * length + "\n"
        return image
