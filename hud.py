from engine.gameObject import GameObject
from engine.image import Image
import characters
import level

class Hud(GameObject):
    def __init__(self, x, y, image = ([[]]), collision = False):
        super().__init__(x, y, Image([[]]), collision)

    def update(self, game):
        scene = game.curScene

        player = scene.getPlayer()

        image = ""
        image += "Health " + str(player.health) + "/" + str(player.maxHealth)
        image += " Gold 0"
        image += "\n"


        self.image = Image.stringToImage(image)
