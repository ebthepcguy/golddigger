from engine.game import Game
import menu

def main():
    game = Game("Gold Digger", 75,40)
    m = menu.MainMenu()
    game.run(m)

main()
