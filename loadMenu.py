from engine.scene import Scene
from engine.image import Image
from engine.keyboard import Keyboard, KeyCode
from engine.gameObject import GameObject
from engine.util import clamp

import pickle, shelve
import levelEditor, level, mainMenu

class LoadMenu(Scene):

    def __init__(self, title, fileName, scene):
        super().__init__()
        image = Image.stringToImage(title)
        self.__title = GameObject(3, 1, image)

        self.__fileName = fileName
        self.__lastScene = scene

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

        image = Image.stringToImage("Press ESC to return")
        self.addGameObject( GameObject(50, 39, image) )

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
        elif (kb.keyPressed(KeyCode.ESC)):
            if ( self.__fileName == game.SAVE_FOLDER + game.LEVEL_FILE ):
                editor = levelEditor.LevelEditor()
                editor.gameObjects = self.__lastScene.gameObjects
                game.loadScene(editor)
            elif ( self.__fileName == game.SAVE_FOLDER + game.GAME_FILE ):
                if ( isinstance(self.__lastScene, mainMenu.MainMenu) ):
                    game.loadScene(self.__lastScene)
                else:
                    l = level.Level()
                    l.gameObjects = self.__lastScene.gameObjects
                    game.loadScene(l)

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

        if ( self.__fileName == game.SAVE_FOLDER + game.LEVEL_FILE ):
            editor = levelEditor.LevelEditor()
            editor.gameObjects = data
        elif ( self.__fileName == game.SAVE_FOLDER + game.GAME_FILE ):
            l = level.Level()
            l.gameObjects = data

        s.close()

        if ( self.__fileName == game.SAVE_FOLDER + game.LEVEL_FILE ):
            game.loadScene(editor)
        elif ( self.__fileName == game.SAVE_FOLDER + game.GAME_FILE ):
            game.loadScene(l)
