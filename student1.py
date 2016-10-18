from constants import *
from snake import Snake
from node import Node
from state1 import State
import math
import random
import heapq

class StudentAgent(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0)):
        super().__init__(body,direction,name="StudentAgent1")

    #Where we update self.direction
    def updateDirection(self,maze):
        opponentPos = [ x for x in maze.playerpos if x != self.body ]
        state = State( self.body, opponentPos, maze.obstacles, maze.foodpos)
        c = self.aStarSearch(state)
        while c.parent.parent != None: 
            c = c.parent

        self.direction = c.action  
    

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

    #Return True if state is goal
    def isGoal(self,state):
        return state.playerPos[0] == state.foodpos

    #Returns expected value (has to minimize the actual steps it takes to get to goal)
    def heuristic(self,state):
        return self.manhattan_distance(state.playerPos[0],state.foodpos)

    def manhattan_distance(self,x,y):
        return min(abs(y[0]-x[0]), self.mapsize[0]-1-abs(y[0]-x[0]))  +  min(abs(y[1]-x[1]), self.mapsize[1]-1-abs(y[1]-x[1]))
 
    #Returns node
    def aStarSearch(self,state):
        node = Node(state,0,self.heuristic(state),None,None)
        frontier = []
        heapq.heappush(frontier, node)
        explored = []
        while True:
            if frontier == []:
                return None
            node = heapq.heappop(frontier)
            if self.isGoal(node.state):
                return node
           
            if node.state not in explored:
                explored += [node.state]
            
            for action in self.actions(node.state):
                child = Node( self.result(node.state, action) , node.cost+1, self.heuristic(node.state), action, node)
                if child.state not in explored and child not in frontier:
                    heapq.heappush(frontier, child)

                elif child in frontier:
                    i = frontier.index(child)
                    if frontier[i].cost > child.cost:
                        frontier.remove(frontier[i])
                        heapq.heapify(frontier)
                        heapq.heappush(frontier, child)
