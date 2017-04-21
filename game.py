import os

from characters import *
from util import Vector
from level import Level, Map
from keyboard import Keyboard, KeyCode


# Create Static Vectors
UP = Vector(0,-1)
DOWN = Vector(0,1)
LEFT = Vector(-1,0)
RIGHT = Vector(1,0)
STAY = Vector(0,0)


def update(level, keyboard):
    char = level.getChar()
    char.setDirToMove(STAY)

    # Check if the user pressed any keys
    keyboard.update()

    # If button pressed was "w"
    if keyboard.keyPressed(KeyCode.w):
        char.setDirToMove(UP)

    # If button pressed was "s"
    elif keyboard.keyPressed(KeyCode.s):
        char.setDirToMove(DOWN)

    # If button pressed was "a"
    elif keyboard.keyPressed(KeyCode.a):
        char.setDirToMove(LEFT)

    # If button pressed was "d"
    elif keyboard.keyPressed(KeyCode.d):
        char.setDirToMove(RIGHT)
    # If button pressed was anything else
    else:
        char.setDirToMove(STAY)




    oldMap = str(level.getMap())
    level.updateMap()
    # Print map if it is different than oldMap
    if oldMap != str(level.getMap()):
        os.system('cls')
        print(level.getMap())
        print(level.getChar().displayStatus())


# Main
def main():
    # Set window to spicific size
    os.system("mode con cols=90 lines=40")

    # Create Character for level
    char = Character("Bob", 10)
    # Create Map for level
    map = Map(char, 30, 30)
    # Create Level
    level = Level(char, map)

    keyboard = Keyboard()

    print(level.getMap())
    print(level.getChar().displayStatus())
    while(True):
        update(level, keyboard)




main()
