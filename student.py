import math
import functools
from constants import *
from snake import Snake
from state import State

class StudentAgent(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0)):
        super().__init__(body,direction,name="StudentAgent")

    #Given a state determines if its terminal
    def cutoff_test(self,depth,state):
        return depth > 2 or state.playerDead or state.opponentDead or state.foodpos in (state.player[0],state.opponent[0])

    #Given a state returns its utility value
    def eval(self,state):
        if state.playerDead:
            return -math.inf
        if state.opponentDead:
            return math.inf
        
        val = -self.manhattan_distance(state.player[0], state.foodpos)
        val += self.manhattan_distance(state.opponent[0], state.foodpos)

        return val

    def manhattan_distance(self,x,y):
        return min(abs(y[0]-x[0]), self.mapsize[0]-1-abs(y[0]-x[0]))  +  min(abs(y[1]-x[1]), self.mapsize[1]-1-abs(y[1]-x[1]))

    #Returns all valid player moves
    def playerActions(self):
        return [ left, up, right, down ]

    #Returns all valid opponent moves
    def opponentActions(self):
        return [ left, up, right, down ]

    def update(self,points=None, mapsize=None, count=None):
       self.lpoints = points
       self.mapsize = mapsize
       self.count = count

    def updateDirection(self,maze):
        state = State(maze,self) 
        val_action = [ ( self.min_value( state.playerResult( action ) , -math.inf, math.inf ), action ) for action in self.playerActions() ]
        val_action = functools.reduce( lambda x, y: x if x[0] > y[0] else y, val_action )
        self.direction = val_action[1]

    def max_value(self,state,alpha,beta,depth = 0):
        if self.cutoff_test(depth, state):
            return self.eval(state)
        v = -math.inf
        for action in self.playerActions():
            m_value = self.min_value( state.playerResult( action ), alpha, beta, depth + 1 )
            v = max(v,m_value)
            if v >= beta:
                return v
            alpha = max(v,alpha)
        return v

    def min_value(self,state,alpha,beta,depth = 0):
        if self.cutoff_test(depth, state):
            return self.eval(state)
        v = math.inf
        for action in self.opponentActions():
            M_value = self.max_value( state.opponentResult( action ), alpha, beta, depth + 1 )
            v = min(v,M_value)
            if v <= alpha:
                return v
            beta = min(v,beta)
        return v
