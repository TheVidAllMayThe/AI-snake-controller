from snake import Snake
from constants import *
from heapq import *
import pygame
from node import Node
from functools import reduce

class area:
    def __init__(minX,maxX,minY,maxY,obstacles):
        self.borders = [ (minX,maxX), (minY,maxY) ]
        self.gateways = {}
        #Upper gateway
        temp = []
        for x in range(minX,maxX+1):
            if (x,minY) not in obstacles and (x,minY) + up not in obstacles and x != maxX:
                temp += [(x,minY)]
            elif temp = []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = up
                self.gateways[temp[-1]] = up
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = up
                temp = []

        #Lower gateway
        temp = []
        for x in range(minX,maxX+1):
            if (x,maxY) not in obstacles and (x,maxY) + down not in obstacles and x != maxX:
                temp += [(x,maxY)]
            elif temp = []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = down
                self.gateways[temp[-1]] = down
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = down
                temp = []

        #Left gateway
        temp = []
        for y in range(minY,maxY+1):
            if (minX,y) not in obstacles and (minX,y) + left not in obstacles and y != maxY:
                temp += [(minX,y)]
            elif temp = []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = left
                self.gateways[temp[-1]] = left
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = left
                temp = []

        #Right gateway
        temp = []
        for y in range(minY,maxY+1):
            if (maxX,y) not in obstacles and (maxX,y) + right not in obstacles and y != maxY:
                temp += [(maxX,y)]
            elif temp = []:
                pass
            elif len(temp) > 5:
                self.gateways[temp[0]] = right
                self.gateways[temp[-1]] = right
                temp = []
            else:
                self.gateways[temp[len(temp)//2]] = right
                temp = []

class student(Snake):
    def __init__(self, body=[(0,0)] , direction=(1,0),name="Pizza Boy aka Robot"):
        super().__init__(body,direction,name=name)
        self.node = None

    def update(self,points=None, mapsize=None, count=None, agent_time=None):
        self.agent_time = agent_time
        self.nOpponents = len(points) - 1
        self.mapsize = mapsize
        if self.nOpponents == 0:
            self.opponentPoints = 0
        else:
            self.opponentPoints = [x[1] for x in points if x[0] != self.name][0]

    def updateDirection(self,maze):
        opponentAgent = [x for x in maze.playerpos if x not in self.body]
        mazedata = (self.body[:],opponentAgent,maze.obstacles[:],maze.foodpos) #Search for food
        finalNode = self.aStar(mazedata)
        self.obstacles = maze.obstacles[:]
        self.direction = finalNode.getAction()

    def valid_actions(self,mazedata,points,oppPoints):
            validDirections = []
            occupiedPositions = mazedata[2] + mazedata[1][:-1] + mazedata[0]
            directions = (up, down, right, left)
            if self.nOpponents != 0 and points <= oppPoints:
                for x in directions: #Remover casos de colisão caso estejamos a perder
                    occupiedPositions += [((mazedata[1][0][0]+x[0])%self.mapsize[0], (mazedata[1][0][1]+x[1])%self.mapsize[1])]

            for x in directions:
                if ((mazedata[0][0][0]+x[0])%self.mapsize[0], (mazedata[0][0][1]+x[1])%self.mapsize[1]) not in occupiedPositions:
                    validDirections += [x]
            return validDirections

    def distance(self,pos1, pos2):
        return min(abs(pos2[0]-pos1[0]), (self.mapsize[0])-1-abs(pos2[0]-pos1[0]))  +  min(abs(pos2[1]-pos1[1]), self.mapsize[1]-1-abs(pos2[1]-pos1[1]))

    def isGoal(self,mazedata):
        oppActions = [False]
        if self.nOpponents > 0:
            oppMazedata = (mazedata[1],mazedata[0],mazedata[2],mazedata[3])
            oppActions = [self.valid_actions(self.result(oppMazedata,x),self.opponentPoints,self.points) == [] for x in self.valid_actions(oppMazedata,self.opponentPoints,self.points)]
        return mazedata[0][0] == mazedata[3] or any(oppActions)

    def result(self,mazedata, action):
        newX = (mazedata[0][0][0]+action[0]+self.mapsize[0])%(self.mapsize[0])
        newY = (mazedata[0][0][1]+action[1]+self.mapsize[1])%(self.mapsize[1])
        playerpos = [(newX, newY)]
        playerpos += mazedata[0][:-1]
        mazedata = (playerpos,mazedata[1],mazedata[2],mazedata[3])
        return mazedata


    def aStar(self, mazedata,node = None):
        s = pygame.time.get_ticks()
        actions = self.valid_actions(mazedata,self.points,self.opponentPoints)
        if node == None:
            node = Node(mazedata, 0, self.distance(mazedata[0][0],mazedata[3]),actions[0] if actions != [] else self.direction,None)
        frontier = []
        heappush(frontier, node)
        explored = []
        while (pygame.time.get_ticks() - s) < (self.agent_time*0.9):
            if frontier == []:
                return node
            node = heappop(frontier)

            if self.isGoal(node.maze) and self.valid_actions(self.result(mazedata,node.getAction()),self.points,self.opponentPoints) != []:
                return node

            if node.maze[0][0] not in explored:
                explored += [(node.maze[0][0],node.action)]
            for x in self.valid_actions(node.maze,self.points,self.opponentPoints):
                result = self.result(node.maze,x)
                child = Node(result ,node.costG+1,self.distance(result[0][0],result[3]),x,node)

                if (child.maze[0][0],child.action) not in explored and child not in frontier:
                    heappush(frontier,child)

                elif [x for x in frontier if x == child and x.costG > child.costG] != []:
                    frontier.remove(child)
                    heappush(frontier,child)

        return node
