import msvcrt
from enum import Enum

class Keyboard(object):

    def __init__(self):
        self.__pressedKeys = []

    def update(self):
        # Clear the list of pressed keys
        self.__pressedKeys = []

        # Add all keys pressed since last update to the list
        while(msvcrt.kbhit()):
            self.__pressedKeys.append(ord(msvcrt.getch()))

    def keyPressed(self, key):

        # Get the value from KeyCode if key is a KeyCode
        if(isinstance(key, KeyCode)):
            key = key.value

        # Return if the key was pressed since last update
        if(key in self.__pressedKeys):
            return True
        else:
            return False


class KeyCode(Enum):
    """ A list of keycodes for use with the keyboard object

    Note:
        Currently only includes KeyCode for lowercase keypresses
    """
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = range(97, 123)
