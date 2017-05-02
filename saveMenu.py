from engine.scene import Scene
from engine.image import Image
from engine.keyboard import Keyboard, KeyCode
from engine.gameObject import GameObject

from debugDisplay import DebugDisplay

class SaveMenu(Scene):

    def __init__(self, title, fileName, objectToSave):
        super().__init__()
        image = Image.stringToImage(title)
        self.__title = GameObject(3, 1, image)

        self.__fileName = fileName
        self.__objectToSave = objectToSave

        self.__saveName = ""
        image = Image.stringToImage(self.__saveName)
        self.__nameObject = GameObject(3, 10, image)

        self.addGameObject(self.__title) 
        self.addGameObject(self.__nameObject)   

    def update(self, game):
        kb = game.keyboard
        
        if (kb.keyPressed(KeyCode.ENTER)):
            self.save(game)
        if (kb.keyPressed(KeyCode.BACKSPACE)):
            self.__saveName = self.__saveName[:-1]
        else:
            for key in kb.getPressedKeys():
                self.__saveName += chr(key)

        image = Image.stringToImage("Name  :" + self.__saveName)
        
        self.__nameObject.image = image

    def save(self, game):
        import pickle, shelve
        import levelEditor

        s = shelve.open(self.__fileName)
        s[self.__saveName] = self.__objectToSave.gameObjects

        s.sync()
        s.close()

        editor = self.__objectToSave
        game.loadScene(editor)






