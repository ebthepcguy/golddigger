from util import Vector
import time

# Create Static Vectors
UP = Vector(0,-1)
DOWN = Vector(0,1)
LEFT = Vector(-1,0)
RIGHT = Vector(1,0)
STAY = Vector(0,0)

# Create Character class:
class Character(object):
    # Init:
    def __init__(self, name, health):
        # Create name variable
        self.__name = name
        # Create health variable
        self.__health = health
        # Create maximum air time variable
        self.__maxAirTime = 0.6
        # Create variable to store ven the player jumped
        self.__timeJumped = 0
        # Create direction to move Vector
        self.__dirToMove = STAY
        # Create isFalling bool
        self.__isFalling = False
        # Create isOnGround bool
        self.__isGrounded = True

    def __str__(self):
        if self.__isFalling == True:
            return "~o~"
        else:
            return "-o-"

    # Only for debug
    def displayStatus(self):
        out = ""
        out += "\nName =\t\t" + self.__name
        out += "\nHealth =\t" + str(self.__health)
        out += "\nTime J =\t" + str(self.__timeJumped)
        out += "\nDir =\t\t" + str(self.__dirToMove.getPair())
        out += "\nIsFalling =\t" + str(self.__isFalling)
        out += "\nIsOnGrnd =\t" + str(self.__isGrounded)
        return out

    # Create getters and setters:
    def getDirToMove(self):
        return self.__dirToMove

    def setDirToMove(self, dir):
        self.__dirToMove = dir

    def getTimeInAir(self):
        return time.time() - self.__timeJumped

    # When isFalling is checked:
    def isFalling(self):
        # If the character has beed in the air for too long:
        if self.getTimeInAir() > self.__maxAirTime and self.__isGrounded == False:
            # Set isFalling to true
            self.setFalling(True)
        # Return isFalling
        return self.__isFalling

    # When isFalling is set:
    def setFalling(self, falling):
        self.__isFalling = falling
        # If setting isFalling to true
        if falling == True:
            # Also set isOnGround to true
            self.setGrounded(False)

    def isGrounded(self):
        return self.__isGrounded

    # When setting isOnGround:
    def setGrounded(self, grounded):
        # Store old variable for is OnGround
        oldIsGrounded = self.__isGrounded
        self.__isGrounded = grounded
        # If isOnGround goes from True to False:
        if oldIsGrounded == True and self.__isGrounded == False:
            # Recort time that the jump occured to timeJumped variable
            self.__timeJumped = time.time()
        # If setting isOnGround to True:
        if grounded == True:
            # Also set isFalling to False
            self.setFalling(False)
