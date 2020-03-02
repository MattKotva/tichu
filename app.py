from game import Game
from player import HumanPlayer

player1 = HumanPlayer("Human 1")
player2 = HumanPlayer("Human 2")
player3 = HumanPlayer("Human 3")
player4 = HumanPlayer("Human 4")

game = Game(player1, player2, player3, player4)
game.start()

