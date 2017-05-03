from engine.scene import Scene
from engine.image import Image
from engine.keyboard import Keyboard, KeyCode
from engine.gameObject import GameObject
from debugDisplay import DebugDisplay
import level, levelEditor


class SaveMenu(Scene):

    def __init__(self, title, fileName, scene):
        super().__init__()
        image = Image.stringToImage(title)
        self.__title = GameObject(3, 1, image)

        self.__fileName = fileName
        self.__lastScene = scene

        self.__saveName = ""
        image = Image.stringToImage(self.__saveName)
        self.__nameObject = GameObject(3, 10, image)

        self.addGameObject(self.__title)
        self.addGameObject(self.__nameObject)

        image = Image.stringToImage("Press ESC to return")
        self.addGameObject( GameObject(50, 39, image) )

    def update(self, game):
        kb = game.keyboard

        if (kb.keyPressed(KeyCode.ENTER)):
            self.saveData(game)
        if (kb.keyPressed(KeyCode.BACKSPACE)):
            self.__saveName = self.__saveName[:-1]
        elif (kb.keyPressed(KeyCode.ESC)):
            self.goBack(game)
        else:
            for key in kb.getPressedKeys():
                self.__saveName += chr(key)

        image = Image.stringToImage("Name  :" + self.__saveName)

        self.__nameObject.image = image

    def saveData(self, game):
        import pickle, shelve
        import levelEditor

        s = shelve.open(self.__fileName)
        s[self.__saveName] = self.__lastScene.gameObjects

        s.sync()
        s.close()

        self.goBack(game)

    def goBack(self, game):

        if ( self.__fileName == game.SAVE_FOLDER + game.LEVEL_FILE ):
            editor = levelEditor.LevelEditor()
            editor.gameObjects = self.__lastScene.gameObjects
            game.loadScene(editor)
        elif ( self.__fileName == game.SAVE_FOLDER + game.GAME_FILE ):
            l = level.Level()
            l.gameObjects = self.__lastScene.gameObjects
            game.loadScene(l)
