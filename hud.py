from engine.game import Game
from engine.gameObject import GameObject
from engine.image import Image
import characters
import level

class Hud(GameObject):

    width = None
    height = 9

    def __init__(self, x, y, image = ([[]]), collision = False):
        super().__init__(x, y, Image([[]]), collision)

    def update(self):
        scene = Game.curGame.curScene

        player = scene.player

        image = ""
        image += "Health " + str(player.health) + "/" + str(player.maxHealth)
        image += " Gold " + str(player.gold)
        image += "\n\n"

        image += "Controls: W(Up/Jump), A(Left), S(Down), D(Right)" + "\n"
        image += "Enemies: Basic <<Ö : Pusher ╠═Ö : Digger ««ö" + "\n"
        image += "Blocks: Dirt ▒▒▒ : Gold [$] : Stone [#]" + "\n"
        image += "Pick ups: Gold $ : Health +" + "\n"
        image += "Instructions: Find your way to the exit while collecting gold" + "\n"
        image += "              Moving onto blocks and enemies deals damage" + "\n"



        self.image = Image.stringToImage(image)
