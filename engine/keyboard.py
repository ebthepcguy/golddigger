import msvcrt, os, time
from enum import Enum

class Keyboard(object):

    def __init__(self):
        self.__pressedKeys = []

    def update(self):
        self.__pressedKeys = []
        # Add keys to the list while there are keys in the buffer
        while(msvcrt.kbhit()):
            self.__pressedKeys.append(ord(msvcrt.getch()))

    def keyPressed(self, key):

        # Convert key to int if key is a KeyCode
        if(isinstance(key, KeyCode)):
            key = key.value

        if(key in self.__pressedKeys):
            return True
        else:
            return False

    def getPressedKeys(self):
        return self.__pressedKeys

class KeyCode(Enum):
    # Generate Enums for keys a=97 through z= 123
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = range(97, 123)
    ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE = range(48, 58)
    BACKSPACE = 8
    ENTER = 13
    ESC = 27
    SPACEBAR = 32
    TIMES, PLUS, COMMA, MINUS, PERIOD, DIVIDE = range(42, 48)

"""
kB = Keyboard()

while True:
    os.system("CLS")
    kB.update()
    print(kB.getPressedKeys())
    time.sleep(.5)
"""
