from engine.scene import Scene
from engine.image import Image
from engine.gameObject import GameObject

class Menu(Scene):

    def __init__(self):
        super().__init__()

    def load(self):

        logoString = \
        """
        Gold Digger
        """

        logo  = GameObject(0,0,Image.stringToImage(logoString))

        self.addGameObject(logo)
