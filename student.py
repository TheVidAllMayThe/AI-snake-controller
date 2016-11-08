from snake import Snake
from constants import *
from heapq import *
import pygame
from node import Node
from functools import reduce

class StudentAgent(Snake):
    def __init__(self, body=[(0,0)] , direction=(1,0)): super().__init__(body,direction,name="Pizza Delivery Robot 1.0")

    def update(self,points=None, mapsize=None, count=None, agent_time=None):
        self.agent_time = agent_time
        self.nOpponents = len(points) - 1
        self.mapsize = mapsize
        if self.nOpponents == 0:
            self.opponentPoints = 0
        else:
            self.opponentPoints = [ x[1] for x in points if x[0] != self.name ][0]

    def updateDirection(self,maze):
        studentAgent = self.body
        opponentsAgents = [x for x in maze.playerpos if x not in self.body]
        obstacles = maze.obstacles
        foodpos = maze.foodpos
        mazedata = (studentAgent,opponentsAgents,obstacles,foodpos) #Search for food
        finalNode = self.aStar(mazedata) 
        self.direction = finalNode.getAction()

    def valid_actions(self,mazedata,points,oppPoints):
            validDirections = []
            occupiedPositions = mazedata[2] + mazedata[1][:-1] + mazedata[0]
            directions = (up, down, right, left)
            if self.nOpponents != 0 and points < oppPoints:
                for x in directions: #Remover casos de colisão caso estejamos a perder
                    newX = (mazedata[1][0][0]+x[0]+self.mapsize[0]+1)%(self.mapsize[0]+1)
                    newY = (mazedata[1][0][1]+x[1]+self.mapsize[1]+1)%(self.mapsize[1]+1)
                    occupiedPositions += [(newX, newY)]
            for x in directions:
                newX = (mazedata[0][0][0]+x[0]+self.mapsize[0]+1)%(self.mapsize[0]+1)
                newY = (mazedata[0][0][1]+x[1]+self.mapsize[1]+1)%(self.mapsize[1]+1)
                if (newX, newY) not in occupiedPositions:
                    validDirections += [x]
            return validDirections

    def distance(self,pos1, pos2):
        return min(abs(pos2[0]-pos1[0]), (self.mapsize[0])-1-abs(pos2[0]-pos1[0]))  +  min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1]))

    def isGoal(self,mazedata):
        oppActions = [False]
        if self.nOpponents > 0:
            oppMazedata = (mazedata[1],mazedata[0],mazedata[2],mazedata[3])
            oppActions = [self.valid_actions(self.result(oppMazedata,x),self.opponentPoints,self.points) == [] for x in self.valid_actions(oppMazedata,self.opponentPoints,self.points)]
        if any(oppActions):
            print("Intent to kill!")
        return mazedata[0][0] == mazedata[3] or any(oppActions)

    def result(self,mazedata, action):
        newX = (mazedata[0][0][0]+action[0]+self.mapsize[0]+1)%(self.mapsize[0]+1)
        newY = (mazedata[0][0][1]+action[1]+self.mapsize[1]+1)%(self.mapsize[1]+1)
        playerpos = [(newX, newY)]
        playerpos += mazedata[0][:-1]
        return (playerpos,mazedata[1],mazedata[2],mazedata[3])

    def aStar(self, mazedata):
        s = pygame.time.get_ticks()
        actions = self.valid_actions(mazedata,self.points,self.opponentPoints)
        node = Node(mazedata, 0, self.distance(mazedata[0][0],mazedata[3]),actions[0] if actions != [] else self.direction,None)
        frontier = []
        heappush(frontier, node)
        explored = []
        while (pygame.time.get_ticks() - s) < (self.agent_time*0.9):
            if frontier == []:
                return None
            node = heappop(frontier)

            if self.isGoal(node.maze):
                return node

            if node.maze[0][0] not in explored:
                explored += [node.maze[0][0]]
            for x in self.valid_actions(node.maze,self.points,self.opponentPoints):
                result = self.result(node.maze,x)
                child = Node(result ,node.costG+1,self.distance(result[0][0],result[3]),x,node)

                if child.maze[0][0] not in explored and child not in frontier:
                    heappush(frontier,child)

                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                    frontier.remove(child)
                    heappush(frontier,child)
        return node
