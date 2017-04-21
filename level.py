from characters import Character
from blocks import *
from util import Vector

# Create Static Vectors
UP = Vector(0,-1)
DOWN = Vector(0,1)
LEFT = Vector(-1,0)
RIGHT = Vector(1,0)
STAY = Vector(0,0)

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
