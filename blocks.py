
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
