from testgame import *
from human import HumanSnake
from agent1 import Agent1
from student import StudentAgent
#start the game
if __name__ == "__main__":
    snake=SnakeGame(hor=60, ver=40, tilesize=15, fps=3000)
    snake.setObstacles(15) #level of obstacles
    wins = 0
    draws = 0
    losses = 0
    for i in range(100):
        snake.setPlayers([
            Agent1([snake.playerPos()]),
            StudentAgent([snake.playerPos()]),
        ])
        results = snake.start()
        if results[0][0] > results[1][0]:
            losses += 1
        if results[0][0] == results[1][0]:
            draws += 1
        if results[0][0] < results[1][0]:
            wins +=1
    print("wins: {}".format(wins))
    print("draws: {}".format(draws))
    print("losses: {}".format(losses))
