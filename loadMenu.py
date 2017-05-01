from engine.scene import Scene
from engine.image import Image
from engine.keyboard import Keyboard, KeyCode
from engine.gameObject import GameObject

class LoadMenu(Scene):

    def __init__(self, title, *options):
        super().__init__()
        image = Image.stringToImage(title)
        self.__title = GameObject(0, 0, image)
        self.addGameObject(self.__title)

        self.__options = []
        yPosition = 10
        for option in options:
            image = Image.stringToImage("  " + option)
            gO = GameObject(0, yPosition, image)
            self.__options.append(gO)
            self.addGameObject(gO)
            yPosition += 1

    def update(self, game):
        #kb = game.keyboard
        pass