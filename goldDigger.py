from engine.game import Game
from level import Level
from menu import Menu

def main():
    game = Game("Gold Digger", 75,40)
    level = Level()
    menu = Menu()
    game.run(level)
main()
