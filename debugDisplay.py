from engine.game import Game
from engine.gameObject import GameObject
from engine.image import Image
import characters
import level

class DebugDisplay(GameObject):
    def __init__(self, x, y, image = ([[]]), collision = False):
        super().__init__(x, y, Image([[]]), collision)

    def update(self):

        scene = Game.curGame.curScene
        dt = Game.curGame.deltaTime

        #if(isinstance(scene, level.Level)):
        player = scene.player
        
        image = ""
        image += "Player: (" + str(player.x) + ", " + str(player.y) + ") " + "\n"
        image += "Delta Time: " + str(dt) + "\n"
        image += "Game Objects: " + str(scene.len()) + "\n"
        image += "Player isFalling: " + str(player.falling) + "\n"

        self.image = Image.stringToImage(image)
