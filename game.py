import engine.gameObject, engine.screenBuffer, engine.scene, engine.keyboard
import os, time

class Game(object):

    def __init__(self, title, width, height):
        self.__title = title
        self.__width = width
        self.__height = height
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
            if(tempDeltaTime < 0.00):
                time.sleep(0.00 - tempDeltaTime)

    def quit(self):
        self.__running = False

    def loadScene(self, scene):
        scene.game = self
        self.__curScene = scene
        self.__curScene.load()

    def update(self):
        self.__keyboard.update()
        self.__curScene.update(self)
        self.__curScene.updateGameObjects()

    def draw(self):
        self.__curScene.draw()

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
