from engine.game import Game
from engine.gameObject import GameObject
from engine.image import Image
import characters, level, levelEditor, blocks

class Hud(GameObject):

    width = None
    height = 9

    def __init__(self, x, y, image = ([[]]), collision = False):
        super().__init__(x, y, Image([[]]), collision)

    def update(self):
        scene = Game.curGame.curScene

        player = scene.player

        image = ""

        if isinstance(scene, level.Level):
            image += "Health " + str(player.health) + "/" + str(player.maxHealth)
            image += " Gold " + str(player.gold)
            image += "\n\n"

            image += "Controls:  W(Up/Jump) │ A(Left)    │ S(Down)    │ D(Right)" + "\n"
            image += "Enemies:   Basic <<Ö  │ Pusher ╠═Ö │ Digger ««ö │" + "\n"
            image += "Blocks:    Dirt  ▒▒▒  │ Gold   [$] │ Stone  [#] │ Bomb  [3]" + "\n"
            image += "Pick ups:  Gold   $   │ Health  +  │ Press ESC for Pause/Menu" + "\n"
            image += "Instructions: Find your way to the exit while collecting gold" + "\n"
            image += "              Moving onto blocks and enemies deals damage" + "\n"

        if isinstance(scene, levelEditor.LevelEditor):

            gameObjects = scene.getGameObjectsAtPos(player.x, player.y)

            gameObject = None
            for gO in gameObjects:
                if gO != player and not isinstance(gO, blocks.EditMarker):
                    gameObject = gO

            if isinstance(gameObject, characters.Enemy):
                pass
            elif isinstance(gameObject, blocks.Block):
                pass

            if gameObject:
                image += str(gameObject)

            image += "\n"
            image += "    Controls:" + "\n"
            image += "    W) (Up)   │ A) (Left)  │ S) (Down) │ D) (Right)" + "\n"
            image += "    0) Delete │ .) [3]     │ ENTER) Explode Bomb "  + "\n"
            image += "    1) ███    │ 2) ▒▒▒     │ 3) [#] "  + "\n"
            image += "    4) [$]    │ 5)  $      │ 6)  +  "  + "\n"
            image += "    7) [P]    │ 8) [D]     │ 9) ö>>    │ Press ESC for Pause/Menu"  + "\n"
            image += "Move around and place blocks to make your own custom level"

        self.image = Image.stringToImage(image)
