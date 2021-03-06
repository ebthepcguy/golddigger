import engine.gameObject, engine.screenBuffer, engine.scene, engine.keyboard
import os, time

class Game(object):

    MIN_DELTA_TIME = 0.15 # Minimum time between frames
    curGame = None
    width = 0
    height = 0

    def __init__(self, title, width, height):
        Game.curGame = self
        Game.width = width
        Game.height = height

        self.__title = title
        self.__screenBuffer = engine.screenBuffer.ScreenBuffer(width, height)
        self.__keyboard = engine.keyboard.Keyboard()
        self.__curScene = None
        self.__running = False
        self.__deltaTime = 0 # Time between frames

        # Setup console window
        os.system("title " + title)
        os.system("mode con: cols=" + str(width + 1) + " lines=" + str(height + 1))

    def run(self, scene):
        self.__running = True
        self.loadScene(scene)

        prevTime = time.time()

        while(self.__running):
            # Get time between frames
            curTime = time.time()
            self.__deltaTime = curTime - prevTime
            prevTime = curTime

            self.update()
            self.draw()

            # Artificially limit framerate to reduce flashing
            # Frame must take atleast 0.0333 seconds to update and draw
            tempDeltaTime = time.time() - prevTime
            if(tempDeltaTime < self.MIN_DELTA_TIME):
                time.sleep(self.MIN_DELTA_TIME - tempDeltaTime)

    def quit(self):
        self.__running = False

    def loadScene(self, scene):

        if(self.__curScene):
            self.__curScene.quit()
        # Update keyboard to clear out any keys pressed from last scene
        self.__keyboard.update()
        self.__curScene = scene
        self.__curScene.load()

    def update(self):
        self.__keyboard.update()
        self.__curScene.update()
        self.__curScene.updateGameObjects()

    def draw(self):
        self.__curScene.draw(self)

    @property
    def curScene(self):
        return self.__curScene

    @property
    def deltaTime(self):
        return self.__deltaTime

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def keyboard(self):
        return self.__keyboard

    @property
    def screenBuffer(self):
        return self.__screenBuffer
