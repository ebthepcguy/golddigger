from engine.game import Game
from level import Level
from mainMenu import MainMenu

def main():
    game = Game("Gold Digger", 75,40)
    menu = MainMenu()
    game.run(menu)
main()