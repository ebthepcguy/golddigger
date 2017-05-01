from engine.scene import Scene
from engine.image import Image
from engine.keyboard import Keyboard, KeyCode
from engine.gameObject import GameObject

from debugDisplay import DebugDisplay

class SaveMenu(Scene):

    def __init__(self, title, objectToSave, fileName):
        super().__init__()
        image = Image.stringToImage(title)
        self.__title = GameObject(3, 1, image)

        self.__objectToSave = objectToSave
        self.__fileName = fileName

        self.__saveName = ""
        image = Image.stringToImage(self.__saveName)
        self.__nameObject = GameObject(3, 10, image)

        self.addGameObject(self.__title) 
        self.addGameObject(self.__nameObject)   

    def update(self, game):
        kb = game.keyboard
        
        if (kb.keyPressed(KeyCode.ENTER)):
            self.save(game)
        
        for key in kb.getPressedKeys():
            self.__saveName += chr(key)

        image = Image.stringToImage("Name  :" + self.__saveName)
        
        self.__nameObject.image = image

    def save(self, game):
        import pickle, shelve
        import levelEditor

        shelve = shelve.open(self.__fileName)
        shelve["self.__saveName"] = self.__objectToSave

        shelve.sync()
        shelve.close()

        editor = self.__objectToSave
        game.loadScene(editor)






