from constants import *
from snake import Snake
from node import Node
from state1 import State
import random

class StudentAgent(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0)):
        super().__init__(body,direction,name="StudentAgent")

    #Where we update self.direction
    def updateDirection(self,maze):
        opponentPos = [ x for x in maze.playerpos if x != self.body ]
        state = State( self.body, opponentPos, maze.obstacles, maze.foodpos)
        self.direction = self.actions(state)[random.randrange(len(self.actions(state)))] 
        #self.direction = self.aStarSearch(state).action  

    #Gets some game information
    def update(self,points=None, mapsize=None, count=None):
        self.playerPoints = points
        self.mapsize = mapsize
        self.count = count

    #Determine result of an action
    def result(self,state,action):
        playerPos = [ ((x[0]+action[0])%self.mapsize[0],(x[1]+action[1])%self.mapsize[1]) for x in state.playerPos ] 
        return State(playerPos,state.opponentPos,state.obstacles,state.foodpos)

    #Determine all valid actions
    def actions(self,state):
        actions = [ up, left, down, right ]
        if self.result(state,up).playerPos[0] in state.playerPos + state.opponentPos + state.obstacles:    
            actions.remove(up)
        if self.result(state,left).playerPos[0] in state.playerPos + state.opponentPos + state.obstacles:    
            actions.remove(left)
        if self.result(state,down).playerPos[0] in state.playerPos + state.opponentPos + state.obstacles:    
            actions.remove(down)
        if self.result(state,right).playerPos[0] in state.playerPos + state.opponentPos + state.obstacles:    
            actions.remove(right)
        return actions
    
    #Returns expected value (has to minimize the actual steps it takes to get to goal)
    def heuristic(self,state):
        pass

    #Returns node
    def aStarSearch(self,state):
        pass
