from engine.scene import Scene
from engine.image import Image
from engine.gameObject import GameObject
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp

class Menu(Scene):

    def __init__(self):
        super().__init__()

    def load(self):

        logoString = \
        """

     _____       _     _______ _
    |  __ \     | |   | |  _  (_)
    | |  \/ ___ | | __| | | | |_  __ _  __ _  ___ _ __
    | | __ / _ \| |/ _` | | | | |/ _` |/ _` |/ _ \ '__|
    | |_\ \ (_) | | (_| | |/ /| | (_| | (_| |  __/ |
     \____/\___/|_|\__,_|___/ |_|\__, |\__, |\___|_|
                                  __/ | __/ |
                                 |___/ |___/

        """

        logo  = GameObject(0,0,Image.stringToImage(logoString))
        menuSelect = MenuSelect()

        self.addGameObject(logo)
        self.addGameObject(menuSelect)

class MenuSelect(GameObject):

    image1 = Image.stringToImage(\
    """
    > Launch GoldDigger    Launch Level Editor

      Load Saved Game      Exit Game
    --------------------------------------------
    """)

    image2 = Image.stringToImage(\
    """
      Launch GoldDigger  > Launch Level Editor

      Load Saved Game      Exit Game
    --------------------------------------------
    """)

    image3 = Image.stringToImage(\
    """
      Launch GoldDigger    Launch Level Editor

    > Load Saved Game      Exit Game
    --------------------------------------------
    """)

    image4 = Image.stringToImage(\
    """
      Launch GoldDigger    Launch Level Editor

      Load Saved Game    > Exit Game
    --------------------------------------------
    """)

    def __init__(self):

        image = \
        """
        > Launch GoldDigger    Launch Level Editor

          Load Saved Game      Exit Game
        --------------------------------------------
        """

        image = Image.stringToImage(image)

        super().__init__(0, 15, image)

        self.__menuPosX = 0
        self.__menuPosY = 0

    def update(self, game):
        kb = game.keyboard

        # To remove later: Needed for testing
        #self.startEditor(game)

        if(kb.keyPressed( KeyCode.w )):
            self.move(0,-1)
        elif(kb.keyPressed( KeyCode.s )):
            self.move(0,1)
        elif(kb.keyPressed( KeyCode.a )):
            self.move(-1,0)
        elif(kb.keyPressed( KeyCode.d )):
            self.move(1,0)
        elif(kb.keyPressed( KeyCode.ENTER )):
            self.select(game)

        if(self.__menuPosX == 0 and self.__menuPosY == 0):
            self.image = self.image1
        elif(self.__menuPosX == 1 and self.__menuPosY == 0):
            self.image = self.image2
        elif(self.__menuPosX == 0 and self.__menuPosY == 1):
            self.image = self.image3
        elif(self.__menuPosX == 1 and self.__menuPosY == 1):
            self.image = self.image4


    def select(self, game):
        if(self.__menuPosX == 0 and self.__menuPosY == 0):

            self.startGame(game)

        elif(self.__menuPosX == 1 and self.__menuPosY == 0):

            self.startEditor(game)

        elif(self.__menuPosX == 0 and self.__menuPosY == 1):
            pass
        elif(self.__menuPosX == 1 and self.__menuPosY == 1):
            game.quit()

    def move(self, x, y):
        self.__menuPosX = clamp(self.__menuPosX + x, 0, 2)
        self.__menuPosY = clamp(self.__menuPosY + y, 0, 2)

    def startGame(self, game):
        import level
        level = level.Level()
        game.loadScene(level)

    def startEditor(self, game):
        import levelEditor
        editor = levelEditor.LevelEditor()
        game.loadScene(editor)

