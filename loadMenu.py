from engine.scene import Scene
from engine.image import Image
from engine.keyboard import Keyboard, KeyCode
from engine.gameObject import GameObject
from engine.util import clamp

import pickle, shelve
import levelEditor

class LoadMenu(Scene):

    def __init__(self, title, fileName):
        super().__init__()
        image = Image.stringToImage(title)
        self.__title = GameObject(3, 1, image)

        self.__fileName = fileName

        s = shelve.open(self.__fileName)
        names = list(s.keys())

        self.__nameObjects = []
        y = 3
        for name in names:
            image = Image.stringToImage("  " + name)
            t = ( GameObject(3, y, image), name )
            self.__nameObjects.append(t)
            y += 1

        self.addGameObject(self.__title) 

        for nameObject in self.__nameObjects:
            self.addGameObject(nameObject[0])

        s.close()

        self.__activeOption = 0

    def update(self, game):
        kb = game.keyboard
        
        if (kb.keyPressed(KeyCode.ENTER)):
            index = 0 
            for nameObject in self.__nameObjects:
                if self.__activeOption == index: 
                    self.loadData(game, nameObject[1])
                index += 1 
        elif (kb.keyPressed(KeyCode.w)):
            self.__activeOption = clamp(self.__activeOption - 1, 0, len(self.__nameObjects))
        elif (kb.keyPressed(KeyCode.s)):
            self.__activeOption = clamp(self.__activeOption + 1, 0, len(self.__nameObjects))

        self.updateNames()

    def updateNames(self):
        index = 0
        for nameObject in self.__nameObjects:
            if self.__activeOption == index:
                image = Image.stringToImage("> " + nameObject[1])
            else:
                image = Image.stringToImage("  " + nameObject[1])
            index += 1 
            nameObject[0].image = image

    def loadData(self, game, nameOfData):
        s = shelve.open(self.__fileName)

        data = s[nameOfData]

        editor = levelEditor.LevelEditor()
        editor.gameObjects = data
        
        s.close()

        game.loadScene(editor)