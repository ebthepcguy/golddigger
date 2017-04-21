import msvcrt
import time
import os

# Create Vector object to easily keep track of locations on map
class Vector(object):
    # Each Vector has an x and y coord and cannot be changed
    def __init__(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__pair = (x,y)

    # Vectors can be added togeter by combineing thier x and y values
    def __add__(self, other):
        x = self.__x + other.__x
        y = self.__y + other.__y
        return Vector(x,y)

    # Make Vectors return true when they are both the same
    def __eq__(self, other):
        x = self.__x - other.__x
        y = self.__y - other.__y
        if x == 0 and y == 0:
            return True
        else:
            return False

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getPair(self):
        return self.__pair

# Create Map class
class Map(object):
    # Init:
    def __init__(self, char, w = 10, d = 10):
        # Create Map width variable
        self.__width = w
        # Create Map depth variable
        self.__depth = d
        # Create list of valid Vectors using width and depth
        self.__vecList = []
        for y in range(0, self.__depth):
            for x in range(0, self.__width):
                vec = Vector(x,y)
                self.__vecList.append(vec)
        # Create dictonary of objects using Vectors as the key
        self.__objectAtCoord = {}
        # Populate dictionary with blocks and spawn the player near the top (Generate Map)
        self.generateMap(char)

    # To-string:
    def __str__(self):
        # Use to-string to display map contents on screen
        out = ""
        for y in range(0, self.__depth):
            for x in range(0, self.__width):
                out += str(self.__objectAtCoord[(x,y)])
            out += "\n"
        return out

    def getVecList(self):
        return self.__vecList

    # Generate Map:
    def generateMap(self, char):
        # Iterate through map Dictionary and place Air blocks on top with dirt and ore blocks underneath
        for vec in self.getVecList():
            if vec.getY() == 0:
                self.__objectAtCoord[vec.getPair()] = Air()
            else:
                self.__objectAtCoord[vec.getPair()] = Dirt()
        # Also place the player on the top
        self.__objectAtCoord[(5,0)] = char

    def getObjectAtCoord(self, coord = (0,0)):
        return self.__objectAtCoord[coord]

    def setObjectAtCoord(self, coord, obj):
        self.__objectAtCoord[coord] = obj

# Create resource blocks(Air, Dirt ,Iron, Stone)  
class Air(object):
    def __init__(self, health = 0):
        self.__health = health

    def __str__(self):
        return "███"

class Dirt(object):
    def __init__(self, health = 2):
        self.__health = health

    def __str__(self):
        out = ""
        if self.__health == 2:
            out = "░░░"
        elif self.__health == 1:
            out = "▒▒▒"
        return out

    def getHealth(self):
        return self.__health

    def doDamage(self):
        self.__health -= 1

class Stone(object):
    def __init__(self, health = 2):
        self.__health = health

    def __str__(self):
        return "[#]"

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

# Create Level object to store current char and map. Also runs game logic.
class Level(object):
    # Chartacter, Map, and enemy variables
    def __init__(self, char, map):
        assert isinstance(char, Character)
        self.__character = char
        assert isinstance(map, Map)
        self.__map = map

    def getChar(self):
        return self.__character

    def getMap(self):
        return self.__map

    # Go thorugh the levels map to find all objects that need to move:
    def updateMap(self):
        # Create Vector for Character location
        charVec = 0
        # Create Vector List for all stones
        stoneVecList = []
        # Iterate through map to find Character and stone locations
        for vec in self.getMap().getVecList():
            obj = self.getMap().getObjectAtCoord( vec.getPair() )
            if type(obj) is Character:
                charVec = vec
            if type(obj) is Stone:
                stoneVecList.append(vec)
        # Update Charater location
        self.updateChar(charVec)
        # Update stone locations
        self.updateStones(stoneVecList)

    # Update the charaters location(pass through current location as a Vector)
    def updateChar(self, currentVec):
        # Get the direction that the character wants to move
        dir = self.getChar().getDirToMove()

        # Find out what the block below the Character is:
        vecBelow = currentVec + DOWN
        if vecBelow in self.getMap().getVecList():
            blockBelow = self.getMap().getObjectAtCoord( vecBelow.getPair() )
            # If the block is Air
            if type( blockBelow ) is Air:
                # Set the Character to isOnGround = False
                self.getChar().setGrounded(False)
            # Else
            else:
                # Set the Character to isOnGround = True
                self.getChar().setGrounded(True)
        # If there is no block below them(of the map):
        else:
            # Set the Character to isOnGround = True
            self.getChar().setGrounded(True)

        # If the character is falling set thier derection to down:
        if self.getChar().isFalling() == True:
            dir = DOWN

        # Find the block that the Character wants to move to:
        vecToMoveInto = dir + currentVec
        if vecToMoveInto in self.getMap().getVecList():
            block = self.getMap().getObjectAtCoord( vecToMoveInto.getPair() )
            # If the Character wants to move up:
            if dir == UP:
                # If the block is Dirt:
                if type( block ) is Dirt:
                    # And the Character is not falling
                    if self.getChar().isFalling() == False:
                        # Damage the block
                        block.doDamage()
                        # If the block is at zero health:
                        if block.getHealth() == 0:
                            # Destroy block
                            self.getMap().setObjectAtCoord( vecToMoveInto.getPair() , Air() )
                # If the block is Air:
                if type( block ) is Air:
                    # And the Character is on the ground:
                    if self.getChar().isGrounded() == True:
                        #Jump in the air
                        self.getMap().setObjectAtCoord( currentVec.getPair() , Air() )
                        self.getMap().setObjectAtCoord( vecToMoveInto.getPair() , self.getChar() )
            # If the character wants to move in any other direction(other than up):
            elif dir != STAY:
                # If the block is Dirt:
                if type( block ) is Dirt:
                    # Damage the block
                    block.doDamage()
                    # If the blocks is at zero health
                    if block.getHealth() == 0:
                        # Destroy block and put the Character in its place
                        self.getMap().setObjectAtCoord( currentVec.getPair() , Air() )
                        self.getMap().setObjectAtCoord( vecToMoveInto.getPair() , self.getChar() )
                # If the block is air:
                elif type( block ) is Air:
                    # Move in that derection
                    self.getMap().setObjectAtCoord( currentVec.getPair() , Air() )
                    self.getMap().setObjectAtCoord( vecToMoveInto.getPair() , self.getChar() )
    
    # Update all of the stone locations(pass through current locations as a Vector list)
    def updateStones(self, stoveVecList):
        i=1

# Create Static Vectors
UP = Vector(0,-1)
DOWN = Vector(0,1)
LEFT = Vector(-1,0)
RIGHT = Vector(1,0)
STAY = Vector(0,0)

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

    # While game is running
    print(level.getMap())
    print(level.getChar().displayStatus())
    while True:
        # If no buttons are being pressed
        while not msvcrt.kbhit():
            oldMap = str(level.getMap())
            # Update map
            level.updateMap()
            # Print map if it is different than oldMap
            if oldMap != str(level.getMap()):
                os.system('cls')
                print(level.getMap())
                print(level.getChar().displayStatus())

            # Reset direction for the character to move
            level.getChar().setDirToMove(STAY)
            
        # If a button was pressed
        while msvcrt.kbhit():
            # Record button press
            input = ord(msvcrt.getch())

        # If button pressed was "w"
        if input == 119:
            char.setDirToMove(UP)
        # If button pressed was "s"
        elif input == 115:
            char.setDirToMove(DOWN)
        # If button pressed was "a"
        elif input == 97:
            char.setDirToMove(LEFT)
        # If button pressed was "d"
        elif input == 100:
            char.setDirToMove(RIGHT)
        # If button pressed was anything else
        else:
            char.setDirToMove(STAY)

main()
