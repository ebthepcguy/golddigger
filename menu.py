from engine.image import Image
from engine.scene import Scene
from engine.gameObject import GameObject
from engine.game import Game
from engine.keyboard import Keyboard, KeyCode
from engine.util import clamp
import pickle, shelve, level, levelEditor

class Menu(Scene):

    SAVE_FOLDER = "save_game_files"
    GAME_FILE = SAVE_FOLDER + "/games"
    LEVEL_FILE = SAVE_FOLDER + "/levels"

    def __init__(self, title, lastScene):
        super().__init__()
        self.__title = title
        self.__lastScene = lastScene
        self.__fileName = None
        self.__titleX = 10
        self.__titleY = 3
        self.__originX = 24
        self.__originY = 15

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def lastScene(self):
        return self.__lastScene

    @property
    def fileName(self):
        return self.__fileName

    @fileName.setter
    def fileName(self, fileName):
        self.__fileName = fileName

    @property
    def originX(self):
        return self.__originX

    @property
    def originY(self):
        return self.__originY

    def load(self):
        super().load()

        self.drawBoarder()

        self.addGameObject( GameObject(self.__titleX, self.__titleY, Image.stringToImage(self.title) ) )

        if not ( isinstance(self, MainMenu) ):
            message = "Press ESC to return"
            x = self.game.width - len(message) - 1
            y = self.game.height - 1
            self.addGameObject( GameObject(x, y, Image.stringToImage(message) ) )

    def update(self, game):
        super().update(game)

        kb = game.keyboard

        if ( kb.keyPressed(KeyCode.ESC) and not isinstance(self, MainMenu) ):
            self.goBack()

    def goBack(self):
        self.game.loadScene(self.lastScene)

    def drawBoarder(self, offset = 1):
        maxX = Game.Width - 1
        maxY = Game.Height - 2
        for y in range(0, Game.Height):
            for x in range(0, Game.Width):

                if x == 0 + offset and y == 0 + offset:
                    self.addShape(x, y, "╔")
                elif x == maxX - offset and y == 0 + offset:
                    self.addShape(x, y, "╗")
                elif x == 0 + offset and y == maxY - offset:
                    self.addShape(x, y, "╚")
                elif x == maxX - offset and y == maxY - offset:
                    self.addShape(x, y, "╝")
                elif (x == 0 + offset or x == maxX - offset) and (y > 0 + offset and y < maxY - offset):
                    self.addShape(x, y, "║")
                elif (y == 0 + offset or y == maxY - offset) and (x > 0 + offset and x < maxX - offset):
                    self.addShape(x, y, "═")

    def addShape(self, x, y, char):
        image = Image.stringToImage(char)
        gO = GameObject(x, y, image)
        self.addGameObject(gO, 2)

class SaveMenu(Menu):

    def __init__(self, title, lastScene):
        super().__init__(title, lastScene)
        self.__inputText = ""
        self.__inputAria = None
        self.__maxTextLength = 15

    def load(self):
        super().load()

        self.__inputAria = InputAria(self.originX, self.originY, self.__inputText)
        self.addGameObject( self.__inputAria )

    def update(self, game):
        super().update(game)

        kb = game.keyboard

        if (kb.keyPressed(KeyCode.ENTER)):
            if self.__inputText:
                self.saveData(game)
        elif (kb.keyPressed(KeyCode.BACKSPACE)):
            self.__inputText = self.__inputText[:-1]
        elif not (kb.keyPressed(KeyCode.SPACEBAR)):
            for key in kb.getPressedKeys():
                self.__inputText += chr(key)

        self.__inputText.strip()

        while ( len(self.__inputText) > self.__maxTextLength ):
            self.__inputText = self.__inputText[:-1]

        self.__inputAria.text = self.__inputText

    def saveData(self, game):

        s = shelve.open(self.fileName)
        s[self.__inputText] = self.lastScene.gameObjects

        s.sync()
        s.close()

        self.goBack()



class SelectionMenu(Menu):

    def __init__(self, title, lastScene):
        super().__init__(title, lastScene)
        self.__selector = Selector( self.originX, self.originY )

        self.__options = []

    @property
    def selector(self):
        return self.__selector

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, options):
        self.__options = options

    def load(self):
        super().load()

        self.addGameObject( self.selector )

    def update(self, game):
        super().update(game)

        kb = game.keyboard

        if (kb.keyPressed(KeyCode.w)):
            self.selector.y = clamp( self.selector.y - 1, self.originY, self.originY + len(self.options) )
        elif (kb.keyPressed(KeyCode.s)):
            self.selector.y = clamp( self.selector.y + 1, self.originY, self.originY + len(self.options) )

    def generateOptions(self, optionNames):
        for name in optionNames:
            x = self.originX + 3
            y = self.originY + len(self.options)
            gO = Option(x, y, name)
            self.options.append(gO)
            self.addGameObject(gO)

    def getSelectedOption(self):
        for option in self.options:
            if option.y == self.selector.y:
                return option.text


class MainMenu(SelectionMenu):

    def __init__(self, title = None, lastScene = None):
        title = """
     _____       _     _______ _
    |  __ \     | |   | |  _  (_)
    | |  \/ ___ | | __| | | | |_  __ _  __ _  ___ _ __
    | | __ / _ \| |/ _` | | | | |/ _` |/ _` |/ _ \ '__|
    | |_\ \ (_) | | (_| | |/ /| | (_| | (_| |  __/ |
     \____/\___/|_|\__,_|___/ |_|\__, |\__, |\___|_|
                                  __/ | __/ |
                                 |___/ |___/

        """
        super().__init__(title, lastScene)

    def load(self):
        super().load()

        if not self.hasAny(Option):
            optionNames = ["Start New Game",
                           "Load Saved Game",
                           "Load Custom Level",
                           "Launch Level Editor",
                           "Exit Game"]

            self.generateOptions(optionNames)

    def update(self, game):
        super().update(game)

        kb = game.keyboard

        if (kb.keyPressed(KeyCode.ENTER)):
            selectedOption = self.getSelectedOption()

            if ( selectedOption == self.options[0].text ):

                self.startGame(game)
            elif ( selectedOption == self.options[1].text ):
                l = LoadMenu("Load Saved Game:", self)
                l.fileName = Menu.GAME_FILE
                game.loadScene(l)
            elif ( selectedOption == self.options[2].text ):
                l = LoadMenu("Load Custom Level:", self)
                l.fileName = Menu.LEVEL_FILE
                game.loadScene(l)
            elif ( selectedOption == self.options[3].text ):
                self.startEditor(game)
            elif ( selectedOption == self.options[4].text ):
                game.quit()

    def startGame(self, game):
        s = shelve.open(Menu.LEVEL_FILE)

        try:
            data = s["level_01"]
            l = level.Level()
            l.gameObjects = data
        except:
            l = level.Level()
            l.generate()

        s.close()

        game.loadScene(l)

    def startEditor(self, game):
        import levelEditor
        e = levelEditor.LevelEditor()
        game.loadScene(e)



class LoadMenu(SelectionMenu):

    def __init__(self, title, lastScene):
        super().__init__(title, lastScene)

    def load(self):
        super().load()

        s = shelve.open(self.fileName)
        optionNames = list(s.keys())
        s.close()

        self.generateOptions(optionNames)

    def update(self, game):
        super().update(game)

        kb = game.keyboard

        if (kb.keyPressed(KeyCode.ENTER)):
            selectedOption = self.getSelectedOption()
            self.loadData(selectedOption)

    def loadData(self, selectedOption):
        s = shelve.open(self.fileName)

        data = s[selectedOption]
        if ( isinstance( self.lastScene, levelEditor.LevelEditor ) ):
            e = levelEditor.LevelEditor()
            e.gameObjects = data
        else:
            l = level.Level()
            l.gameObjects = data

        s.close()

        if ( isinstance( self.lastScene, levelEditor.LevelEditor ) ):
            self.game.loadScene(e)
        else:
            self.game.loadScene(l)

class Selector(GameObject):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = Image.stringToImage("=>")

    def update(self, game):
        super().update(game)



class Option(GameObject):

    def __init__(self, x, y, text):
        super().__init__(x, y)
        self.__text = text
        self.image = Image.stringToImage(text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    def update(self, game):
        super().update(game)



class InputAria(GameObject):

    def __init__(self, x, y, text):
        super().__init__(x, y)
        self.__text = text
        self.updateImage()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    def update(self, game):
        super().update(game)

        self.updateImage()

    def updateImage(self):
        self.image = Image.stringToImage("Name  :" + self.__text)
